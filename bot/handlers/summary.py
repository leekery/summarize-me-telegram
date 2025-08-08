from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db.repo import MessageRepo
from bot.services.summarizer import summarize_messages
from bot.db.database import get_connection

router = Router()
repo = MessageRepo()

@router.message(Command("сводка"))
async def summary_cmd(message: Message) -> None:
    chat_id = message.chat.id
    title = message.chat.title or "Без названия"

    # Проверяем, включён ли бот в чате
    with get_connection() as conn:
        cur = conn.execute("SELECT is_enabled FROM chats WHERE chat_id = ?", (chat_id,))
        row = cur.fetchone()
        if row is None:
            conn.execute("INSERT INTO chats (chat_id, title) VALUES (?, ?)", (chat_id, title))
            await message.reply("Чат зарегистрирован. Админ должен включить бота командой /enable")
            return
        if not row["is_enabled"]:
            await message.reply("Бот в этом чате выключен. Попросите админа включить его командой /enable")
            return

    # Получаем последние сообщения
    msgs = await repo.get_last_messages(chat_id=chat_id, limit=50)
    if not msgs:
        await message.reply("Пока нечего суммировать.")
        return

    # Генерируем сводку
    summary_text = await summarize_messages(msgs)

    # Отправляем результат
    await message.reply(summary_text)

    # Помечаем сообщения как использованные
    with get_connection() as conn:
        conn.executemany(
            "UPDATE messages SET is_used = 1 WHERE chat_id = ? AND timestamp = ?",
            [(chat_id, m["timestamp"]) for m in msgs]
        )
