from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.methods import get_all_groups

# Инлай клавиатура для меню useradmina
def create_superadmin_keyboard() -> InlineKeyboardMarkup:
    lexicon_sup = LEXICON()['superadmin']

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=lexicon_sup["groups"], callback_data="groups"),
                   InlineKeyboardButton(text=lexicon_sup["admins"], callback_data="admins"))

    return kb_builder.as_markup()

# Инлай клавиатура для меню суперадмина, которая реагирует на нажатие кнопки 'группы'
def create_superadmin_keyboard() -> InlineKeyboardMarkup:
    lexicon_sup = LEXICON()['superadmin']

    # Получаем список групп из базы данных
    data = get_all_groups()

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=name, callback_data=f'group_id_{group_id}') for group_id, name, password in data], width=1)
    kb_builder.row(InlineKeyboardButton(text=lexicon_sup, callback_data=f'group_id_{group_id}'), )

    return kb_builder.as_markup()
