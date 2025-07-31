from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.db.database import get_connection

router = Router()

@router.message(Command("сводка"))
async def handle_summary_command(message: Message):
    chat_id = message.chat.id
    title = message.chat.title or "Без названия"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_enabled FROM chats WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute("INSERT INTO chats (chat_id, title) VALUES (?, ?)", (chat_id, title))
            await message.reply("Registred")
            return
        
        if not row["is_enabled"]:
            await message.reply("Turned off")
            return
        
        await message.reply("Coming soon...")