from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from keyboards.user_kb import *
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_user_to_database
from aiogram.fsm.state import default_state
from filters.filters import IsUserNotHaveGroup

router = Router()

# Хендлер на комманду старт, если нет группы
@router.message(CommandStart(), StateFilter(default_state), IsUserNotHaveGroup())
async def process_start_command_if_not_group(message: Message):
    # Добавление пользователя в базу данных
    await add_user_to_database(message.from_user.id, message.from_user.username)
    await message.answer(text=LEXICON()['user']['havent_group']['text_menu'],
                         reply_markup=create_start_keyboard_if_not_group())


# Хендлер на комманду старт, если нет группы
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    # Добавление пользователя в базу данных
    await message.answer(text=LEXICON()['user']['have_group']['text_menu'],
                         reply_markup=create_start_keyboard())