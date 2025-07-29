from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_name = message.from_user.full_name if message.from_user else "Anonymous"
    await message.answer(f"Hello, {html.bold(user_name)}!") 