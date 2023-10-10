from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_user_group, get_date_group, get_user, get_all_users_by_group


# Инлай клавиатура для меню user, если он не состоит в группе
def create_start_keyboard_if_admin() -> InlineKeyboardMarkup:
    buttons = LEXICON()['admin']['buttons']
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


# Инлай клавиатура для меню admin, где перечислены участники группы
def create_admin_menu_users_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_users']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем всех пользователей группы
    data = get_all_users_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с пользователями в клавиатуру
    kb_builder.row(*[InlineKeyboardButton(text=f'{"👑" if status_admin == 1 else "🎩"} {username} id = {user_id}',
                                          callback_data=f'user_id_{user_id}') for user_id, username, status_admin, group_id in data], width=1)
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


# Инлай клавиатура для меню admin, где перечислены участники группы, которы можно дать права админа
def create_admin_menu_add_admin_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_users']['admin_menu_add_admin']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем всех пользователей группы
    data = get_all_users_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с пользователями в клавиатуру
    kb_builder.row(*[InlineKeyboardButton(text=f'{"👑" if status_admin == 1 else "🎩"} {username} id = {user_id}',
                                          callback_data=f'admin_add_status_admin_{user_id}') for user_id, username, status_admin, group_id in data], width=1)
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


# Инлай клавиатура для меню admin, где перечислены участники группы, которы можно дать права админа
def create_admin_menu_del_admin_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем всех пользователей группы
    data = get_all_users_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с пользователями в клавиатуру
    kb_builder.row(*[InlineKeyboardButton(text=f'{"👑" if status_admin == 1 else "🎩"} {username} id = {user_id}',
                                          callback_data=f'admin_del_status_admin_{user_id}') for user_id, username, status_admin, group_id in data], width=1)
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()