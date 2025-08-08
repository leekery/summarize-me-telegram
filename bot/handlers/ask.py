import time
from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.types import Message
from bot.db.repo import MessageRepo
from bot.services.asker import ask_with_context

router = Router()
repo = MessageRepo()

# Память для cooldown: {chat_id: timestamp}
_last_ask_time = {}

COOLDOWN_SEC = 300  # 5 минут

@router.message(Command("ask"))
async def ask_cmd(message: Message, command: CommandObject):
    chat_id = message.chat.id
    now = time.time()

    # cooldown
    last_time = _last_ask_time.get(chat_id, 0)
    if now - last_time < COOLDOWN_SEC:
        remain = int(COOLDOWN_SEC - (now - last_time))
        await message.reply(f"Подожди ещё {remain} сек. перед следующим вопросом.")
        return

    question = command.args
    if not question:
        await message.reply("Использование: /ask ваш вопрос")
        return

    # последние 100 сообщений без фильтрации is_used
    msgs = await repo.get_recent_messages(chat_id=chat_id, limit=200)

    if not msgs:
        await message.reply("В чате пока нет контекста для ответа.")
        return

    answer = await ask_with_context(msgs, question)

    _last_ask_time[chat_id] = now
    await message.reply(answer)
