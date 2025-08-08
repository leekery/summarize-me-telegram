from aiogram import Router, F
from aiogram.types import Message
from bot.db.repo import MessageRepo

router = Router()
repo = MessageRepo()

# слушаются только группы/супергруппы и только текст, исключая команды
@router.message(
    F.chat.type.in_({"group", "supergroup"}) 
    & F.text 
    & ~F.text.startswith("/")
)
async def collect_messages(message: Message):
    user = message.from_user
    await repo.save_message(
        chat_id=message.chat.id,
        user_id=user.id if user else None,
        user_name=user.full_name if user else "Anonymous",
        text=message.text,
        timestamp=message.date.isoformat(),
    )