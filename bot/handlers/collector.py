from aiogram import Router, F
from aiogram.types import Message
from bot.db.repo import MessageRepo
from bot.db.database import get_connection

router = Router()
repo = MessageRepo()

# слушаются только группы/супергруппы и только текст, исключая команды
@router.message(
    F.chat.type.in_({"group", "supergroup"}) 
    & F.text 
    & ~F.text.startswith("/")
)
async def collect_messages(message: Message):
    chat_id = message.chat.id
    title = message.chat.title or "Без названия"

    # Гарантируем, что чат есть в таблице chats
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO chats (chat_id, title) VALUES (?, ?)",
            (chat_id, title)
        )

    user = message.from_user
    await repo.save_message(
        chat_id=chat_id,
        user_id=user.id if user else None,
        user_name=user.full_name if user else "Anonymous",
        text=message.text,
        timestamp=message.date.isoformat(),
    )
