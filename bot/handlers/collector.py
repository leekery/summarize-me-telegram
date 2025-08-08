from aiogram import Router, F
from aiogram.types import Message
from bot.db.repo import MessageRepo
from bot.db.database import get_connection

router = Router()
repo = MessageRepo()

# слушаются только группы/супергруппы и только текст, исключая команды
@router.message(F.chat.type.in_({"group", "supergroup"}))
async def collect_messages(message: Message):
    # Игнорируем команды (включая медиа с подписью-командой)
    if message.text and message.text.startswith("/"):
        return
    if message.caption and message.caption.startswith("/"):
        return
    chat_id = message.chat.id
    title = message.chat.title or "Без названия"

    # Гарантируем, что чат есть в таблице chats
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO chats (chat_id, title) VALUES (?, ?)",
            (chat_id, title)
        )

    user = message.from_user
    user_name = user.full_name if user else "Anonymous"

    # Определяем контент
    text_content = message.text or message.caption or ""

    if message.photo:
        prefix = "Фото"
    elif message.sticker:
        prefix = "Стикер"
    elif message.video:
        prefix = "Видео"
    elif message.voice:
        prefix = "Голосовое сообщение"
    elif message.document:
        prefix = "Документ"
    else:
        prefix = ""

    # Если есть тип контента, добавляем к тексту
    if prefix:
        if text_content:
            text_content = f"{prefix}: {text_content}"
        else:
            text_content = prefix

    # Если вообще пусто — не сохраняем
    if not text_content.strip():
        return

    await repo.save_message(
        chat_id=chat_id,
        user_id=user.id if user else None,
        user_name=user_name,
        text=text_content,
        timestamp=message.date.isoformat(),
    )
