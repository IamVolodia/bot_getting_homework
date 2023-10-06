from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def send_echo(message: Message):
    await message.answer(f'У меня нет скриптов на эту комманду: {message.text}')