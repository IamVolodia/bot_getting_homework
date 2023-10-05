from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.methods import get_user_group, get_date_group

# Инлай клавиатура для меню user
def create_start_keyboard(user_id) -> InlineKeyboardMarkup:
    callback_group = f"group_id_{get_user_group(user_id)}"
    if callback_group == "group_id_None":
        text_group = LEXICON()['user']['no_exists']
    else:
        text_group = get_date_group(user_id)[1]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=text_group, callback_data=callback_group),
                   InlineKeyboardButton(text=LEXICON()['user']['change_group'], callback_data='change_group'))

    return kb_builder.as_markup()