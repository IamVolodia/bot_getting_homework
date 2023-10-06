from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from keyboards.user_kb import create_start_keyboard
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_user_to_database

router = Router()

# Хендлер на комманду старт
@router.message(CommandStart())
async def process_superadmin_command(message: Message):
    # Добавление пользователя в базу данных
    await add_user_to_database(message.from_user.id, message.from_user.username)
    await message.answer(text=LEXICON()['user']['welcome'],
                         reply_markup=create_start_keyboard(message.from_user.id))