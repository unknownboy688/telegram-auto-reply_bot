# --- bot.py ---
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message

import config
import storage

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("autoreply")


app = Client(
    config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
)


async def human_typing(client: Client, chat_id: int, text: str):
    await client.send_chat_action(chat_id, ChatAction.TYPING)
    delay = min(max(len(text) * 0.03, 0.8), 3.5)
    await asyncio.sleep(delay)
    await client.send_chat_action(chat_id, ChatAction.CANCEL)


@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def on_private(client: Client, message: Message):
    user = message.from_user
    if user is None:
        return

    if user.id == config.OWNER_ID:
        return

    storage.log_message(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        message=message.text or message.caption or "<non-text>",
    )

    if not storage.should_reply(user.id, config.COOLDOWN_SECONDS):
        log.info("cooldown active for %s", user.id)
        return

    try:
        await human_typing(client, message.chat.id, config.OFFLINE_MESSAGE)
        await message.reply_text(config.OFFLINE_MESSAGE)
        log.info("auto-reply sent to %s", user.id)
    except Exception as exc:
        log.exception("reply failed for %s: %s", user.id, exc)


async def main():
    storage.init_db()
    async with app:
        me = await app.get_me()
        log.info("autoreply live as @%s (id=%s)", me.username, me.id)
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
