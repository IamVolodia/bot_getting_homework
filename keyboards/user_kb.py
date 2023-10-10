from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_user_group, get_date_group


# Инлай клавиатура для меню user, если он не состоит в группе
def create_start_keyboard_if_not_group() -> InlineKeyboardMarkup:
    buttons = LEXICON()['user']['havent_group']['buttons']
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


# Инлай клавиатура для меню user, если он состоит в группе
def create_start_keyboard() -> InlineKeyboardMarkup:
    buttons = LEXICON()['user']['have_group']['buttons']
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()