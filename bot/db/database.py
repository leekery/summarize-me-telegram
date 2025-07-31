import sqlite3
from bot.db.models import ChatMessage
from pathlib import Path
from typing import Generator
from config import settings

DB_PATH = Path(settings.db_path)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_cursor() -> Generator[sqlite3.Cursor, None, None]:
    with get_connection() as conn:
        yield conn.cursor()
        conn.commit()

def init_db() -> None:
    """Создаёт таблицы, если они не существуют."""
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id      INTEGER PRIMARY KEY,
            title        TEXT,
            is_enabled   BOOLEAN DEFAULT 0,
            added_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_summary DATETIME
        );

        CREATE TABLE IF NOT EXISTS triggers (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id   INTEGER NOT NULL,
            keyword   TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 0,
            FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id    INTEGER NOT NULL,
            user_id    INTEGER,
            user_name  TEXT,
            text       TEXT NOT NULL,
            timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_used    BOOLEAN DEFAULT 0,
            FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS summaries (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id      INTEGER NOT NULL,
            summary_text TEXT NOT NULL,
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
            message_ids  TEXT,
            FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS settings (
            chat_id      INTEGER PRIMARY KEY,
            max_messages INTEGER DEFAULT 50,
            cooldown_sec INTEGER DEFAULT 300,
            language     TEXT DEFAULT 'ru',
            FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS admins (
            user_id   INTEGER PRIMARY KEY,
            username  TEXT,
            is_root   BOOLEAN DEFAULT 0
        );
        """)