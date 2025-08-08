from bot.db.database import get_connection
from typing import List

class MessageRepo: 
    async def save_message(self, chat_id, user_id, user_name, text, timestamp):
        with get_connection() as conn:
            # Гарантируем, что чат есть в таблице chats
            conn.execute(
                "INSERT OR IGNORE INTO chats (chat_id, title) VALUES (?, ?)",
                (chat_id, user_name if user_name else "Без названия")
            )

            # Сохраняем сообщение
            conn.execute("""
                INSERT INTO messages (chat_id, user_id, user_name, text, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (chat_id, user_id, user_name, text, timestamp))
            conn.commit()

    async def get_last_messages(self, chat_id: int, limit: int = 50) -> List[dict]:
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT user_name, text, timestamp
                FROM messages
                WHERE chat_id = ? AND is_used = 0
                ORDER BY timestamp ASC
                LIMIT ?
            """, (chat_id, limit))
            return [
                {"user_name": row["user_name"], "text": row["text"], "timestamp": row["timestamp"]}
                for row in cursor.fetchall()
            ]

"""
# Example usage

repo = MessageRepo()

# Save a message
await repo.save_message(
    chat_id=123456,
    user_id=7890,
    user_name="some_user",
    text="Hello, world!",
    timestamp="2025-08-07 15:30:00"
)

# Get last 10 unused messages from the chat
messages = await repo.get_last_messages(chat_id=123456, limit=10)

for msg in messages:
    print(f"{msg['timestamp']} — {msg['user_name']}: {msg['text']}")
"""