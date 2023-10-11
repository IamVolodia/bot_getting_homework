from aiogram import Router
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message()
async def send_echo(message: Message):
    await message.answer(f'У меня нет скриптов на эту комманду: {message.text}')

@router.callback_query()
async def process_admin_users_press(callback: CallbackQuery,):
    await callback.answer()