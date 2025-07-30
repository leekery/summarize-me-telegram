from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import html

router = Router()

# /start
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_name = message.from_user.full_name if message.from_user else "Anonymous"
    await message.answer(f"Hello, {html.bold(user_name)}!") 

# /help
@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("/help commands here")