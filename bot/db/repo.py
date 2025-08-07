from bot.db.database import get_connection
from typing import List

class MessageRepo: 
    async def save_message(self, chat_id, user_id, user_name, text, timestamp):
        with get_connection() as conn:
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
                LIMIT ?
            """, (chat_id, limit))
            return [
                {"user_name": row["user_name"], "text": row["text"], "timestamp": row["timestamp"]}
                for row in cursor.fetchall()
            ]