# --- storage.py ---
import sqlite3
import time
from contextlib import contextmanager

DB_PATH = "autoreply.db"

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS replied (
                user_id     INTEGER PRIMARY KEY,
                last_reply  INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inbox (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                username    TEXT,
                first_name  TEXT,
                message     TEXT,
                created_at  INTEGER NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_user ON inbox(user_id)")

def should_reply(user_id: int, cooldown: int) -> bool:
    now = int(time.time())
    with db() as conn:
        row = conn.execute(
            "SELECT last_reply FROM replied WHERE user_id = ?", (user_id,)
        ).fetchone()
        if row is None or now - row["last_reply"] >= cooldown:
            conn.execute(
                "INSERT INTO replied(user_id, last_reply) VALUES(?, ?) "
                "ON CONFLICT(user_id) DO UPDATE SET last_reply = excluded.last_reply",
                (user_id, now),
            )
            return True
    return False

def log_message(user_id: int, username: str, first_name: str, message: str):
    with db() as conn:
        conn.execute(
            "INSERT INTO inbox(user_id, username, first_name, message, created_at) "
            "VALUES(?, ?, ?, ?, ?)",
            (user_id, username, first_name, message, int(time.time())),
        )
