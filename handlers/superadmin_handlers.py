from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from keyboards.superadmin_kb import create_superadmin_keyboard
from config_data.config import load_config
from lexicon.lexicon import LEXICON

router = Router()

@router.message(Command(commands='superadmin'))
async def process_superadmin_command(message: Message):
    if message.from_user.id in load_config().tg_bot.superadmin_ids:
        await message.answer(reply_markup=create_superadmin_keyboard())
    else:
        await message.answer(text=LEXICON()['superadmin']['no_rights'])

@router.callback_query(F.data == 'groups')
async def process_backward_press(callback: CallbackQuery):
    

    await callback.answer()
