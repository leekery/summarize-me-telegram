from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.db.database import get_connection
from bot.db.repo import MessageRepo
from bot.services.summarizer import summarize_messages

router = Router()
repo = MessageRepo()

@router.message(Command("сводка"))
async def summary_cmd(message: Message) -> None:
    chat_id = message.chat.id
    title = message.chat.title or "Без названия"
    with get_connection() as conn:
        cur = conn.execute("SELECT is_enabled FROM chats WHERE chat_id = ?", (chat_id,))
        row = cur.fetchone()
        if row is None:
            conn.execute("INSERT INTO chats (chat_id, title) VALUES (?, ?)", (chat_id, title))
            await message.reply("Чат зарегистрирован. Админ должен включить бота: /enable")
            return
        if not row["is_enabled"]:
            await message.reply("Бот в этом чате выключен. Попросите админа: /enable")
            return

    msgs = await repo.get_last_messages(chat_id=chat_id, limit=50)  # возьмём 50 по умолчанию
    if not msgs:
        await message.reply("Пока нечего суммировать.")
        return

    summary_text = await summarize_messages(msgs)  # вызов сервиса ИИ
    await message.reply(summary_text)