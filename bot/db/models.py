from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    chat_id: int
    user_name: str
    content: str
    timestamp: datetime