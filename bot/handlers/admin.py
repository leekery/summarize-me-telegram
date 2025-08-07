from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import settings
from bot.db.database import get_connection

router = Router()

def is_root(message: Message):
    return message.from_user and message.from_user.id == settings.admin_id

@router.message(Command("enable"))
async def enable_chat(message: Message) -> None:
    if not is_root(message):
        return
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chats(chat_id, title, is_enabled) VALUES (?, ?, 1) "
            "ON CONFLICT(chat_id) DO UPDATE SET is_enabled=1",
            (message.chat.id, message.chat.title or "Без названия"),
        )
    await message.reply("✅ Бот включён в этом чате.")

@router.message(Command("disable"))
async def disable_chat(message: Message) -> None:
    if not is_root(message):
        return
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chats(chat_id, title, is_enabled) VALUES (?, ?, 0) "
            "ON CONFLICT(chat_id) DO UPDATE SET is_enabled=0",
            (message.chat.id, message.chat.title or "Без названия"),
        )
    await message.reply("⛔ Бот выключен в этом чате.")