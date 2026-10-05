# --- config.py ---
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "autoreply_session")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
OFFLINE_MESSAGE = os.getenv(
    "OFFLINE_MESSAGE",
    "Boss abhi offline hain. Aapka message note kar liya gaya hai — online aate hi reply milega."
)
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "3600"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
