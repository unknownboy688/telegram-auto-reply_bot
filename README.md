# Telegram Auto Reply Bot

Offline auto-responder built on Pyrogram. Replies once per user per cooldown window. Every inbound message is logged to SQLite for later review.

## Setup

1. `pip install -r requirements.txt`
2. `cp .env.example .env` and fill in API ID, API Hash, and OWNER_ID
3. First run — Pyrogram will prompt for phone + OTP once, then write `autoreply_session.session`
4. `python bot.py`

## Deploy

- Never commit `.env` or `*.session`
- On a VPS use `systemd` or `pm2` to keep the process alive
- SQLite file `autoreply.db` lives next to the script

## Behavior

- Skips messages from the owner and other bots
- Cooldown enforced per user via `replied` table
- Typing indicator mimics human pacing before the reply lands
- All inbound messages stored in `inbox` table
