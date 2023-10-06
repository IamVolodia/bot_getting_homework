from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_all_groups, get_all_admins

# Инлай клавиатура для меню useradmina
def create_superadmin_keyboard() -> InlineKeyboardMarkup:
    lexicon_super = LEXICON()['superadmin']

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=lexicon_super["groups"], callback_data="groups"),
                   InlineKeyboardButton(text=lexicon_super["admins"], callback_data="admins"))

    return kb_builder.as_markup()


# Инлай клавиатура для меню суперадмина, которая реагирует на нажатие кнопки 'группы'
def create_groups_keyboard() -> InlineKeyboardMarkup:
    lexicon_sup = LEXICON()['superadmin']

    # Получаем список групп из базы данных
    data = get_all_groups()

    kb_builder = InlineKeyboardBuilder()

    if data:
        kb_builder.row(*[InlineKeyboardButton(text=f'{name}', callback_data=f'group_id_{group_id}') for group_id, name, password in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=lexicon_sup["menu_groups"]["empty"], callback_data='empty'))

    kb_builder.row(InlineKeyboardButton(text=lexicon_sup["menu_groups"]["add_group"], callback_data='add_group'),
                   InlineKeyboardButton(text=lexicon_sup["menu_groups"]["delete_group"], callback_data='delete_group'),
                   InlineKeyboardButton(text=LEXICON()["general"]["back"], callback_data='back_in_superadmin'),)

    return kb_builder.as_markup()


# Инлай клавиатура для меню суперадмина, которая реагирует на нажатие кнопки 'админы'
def create_admins_keyboard() -> InlineKeyboardMarkup:
    lexicon_sup = LEXICON()['superadmin']

    # Получаем список групп из базы данных
    data = get_all_admins()

    kb_builder = InlineKeyboardBuilder()

    if data:
        kb_builder.row(*[InlineKeyboardButton(text=f'{username} id = {user_id}', callback_data=f'user_id_{user_id}') for user_id, username in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=lexicon_sup["menu_admins"]["empty"], callback_data='empty'))

    kb_builder.row(InlineKeyboardButton(text=lexicon_sup["menu_admins"]["add_admin"], callback_data='add_admin'),
                   InlineKeyboardButton(text=lexicon_sup["menu_admins"]["delete_admin"], callback_data='delete_admin'),
                   InlineKeyboardButton(text=LEXICON()["general"]["back"], callback_data='back_in_superadmin'),)

    return kb_builder.as_markup()


# Инлай клавиатура для меню суперадмина, которая реагирует на нажатие кнопки 'админы'
def create_delete_admins_keyboard() -> InlineKeyboardMarkup:
    lexicon_sup = LEXICON()['superadmin']

    # Получаем список групп из базы данных
    data = get_all_admins()

    kb_builder = InlineKeyboardBuilder()

    if data:
        kb_builder.row(*[InlineKeyboardButton(text=f'{LEXICON()["general"]["del"]} {username} id = {user_id}', callback_data=f'del_user_id_{user_id}') for user_id, username in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=lexicon_sup["menu_admins"]["empty"], callback_data='empty'))

    kb_builder.row(InlineKeyboardButton(text=LEXICON()["general"]["back"], callback_data='admins'))

    return kb_builder.as_markup()