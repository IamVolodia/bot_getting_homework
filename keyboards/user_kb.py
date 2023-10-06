from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_user_group, get_date_group

# Инлай клавиатура для меню user
def create_start_keyboard(user_id) -> InlineKeyboardMarkup:
    group_id = get_user_group(user_id)
    text_group = get_date_group(group_id)
    callback_group = f"group_id_{group_id}"
    if text_group == None:
        text_group = LEXICON()['user']['no_exists']

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=text_group, callback_data=callback_group),
                   InlineKeyboardButton(text=LEXICON()['user']['change_group'], callback_data='change_group'), width=1)

    return kb_builder.as_markup()