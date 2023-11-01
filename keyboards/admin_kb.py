from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_user_group, get_date_group, get_user, get_all_users_by_group, get_all_subjects_by_group, get_subject_with_homework_for_date


# Инлай клавиатура для меню user, если он не состоит в группе
def create_start_keyboard_if_admin() -> InlineKeyboardMarkup:
    buttons = LEXICON()['admin']['buttons']
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()

#-------------------------клавиатуры миню, где перечислены пользователи группы----------------------------------------------------


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
    # Разделитьель пеользователей от кнопок
    kb_builder.row(InlineKeyboardButton(text=LEXICON()['general']['fence'], callback_data="something"))
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


# Инлай клавиатура для меню admin, где перечислены участники группы, которых можно удалить из группы
def create_admin_menu_del_user_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем всех пользователей группы
    data = get_all_users_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с пользователями в клавиатуру
    kb_builder.row(*[InlineKeyboardButton(text=f'{"♻️ - 👑" if status_admin == 1 else "♻️ - 🎩"} {username} id = {user_id}',
                                          callback_data=f'admin_del_user_{user_id}') for user_id, username, status_admin, group_id in data], width=1)
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


#-------------------------клавиатуры миню по удалению группы----------------------------------------------------


# Инлай клавиатура для меню admin, при нажатии на кнопку Удалить группу
def create_admin_menu_del_group_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_del_group']['buttons']
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=2)

    return kb_builder.as_markup()



# Инлай клавиатура для меню admin, при нажатии на кнопку Удалить группу, второй шанс
def create_admin_menu_del_group_two_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_del_group']['admin_menu_del_group_two']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопку Да, которая будет скрывать в себе коллбек с id группы к удалению
    kb_builder.add(InlineKeyboardButton(text='Да', callback_data=f"admin_del_group_{group_id}"))
    # Генерируем остальные кнопки
    kb_builder.add(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()])

    return kb_builder.as_markup()


#-------------------------клавиатуры миню, где перечислены предметы группы----------------------------------------------------


# Инлай клавиатура для меню admin, где перечислены предметы группы
def create_admin_menu_subjects_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_subjects']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем все предметы группы
    data = get_all_subjects_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с предметами в клавиатуру
    if data:
        kb_builder.row(*[InlineKeyboardButton(text=name,
                                              callback_data=f'admin_subject_id_{subject_id}') for subject_id, name, group_id in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=LEXICON()['admin']['admin_menu_subjects']['no_subjects'], callback_data='something'))
    # Разделитьель пеользователей от кнопок
    kb_builder.row(InlineKeyboardButton(text=LEXICON()['general']['fence'], callback_data="fence"))
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()



# Инлай клавиатура для меню admin, где перечислены предметы группы к удалению
def create_admin_menu_del_subjects_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_subjects']['admin_menu_del_subject']['buttons']
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем все предметы группы
    data = get_all_subjects_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с предметами в клавиатуру
    if data:
        kb_builder.row(*[InlineKeyboardButton(text=f"♻️ {name}",
                                              callback_data=f'admin_del_subject_id_{subject_id}') for subject_id, name, group_id in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=LEXICON()['admin']['admin_menu_subjects']['no_subjects'], callback_data='something'))
    # Разделитьель пеользователей от кнопок
    kb_builder.row(InlineKeyboardButton(text=LEXICON()['general']['fence'], callback_data="fence"))
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()



#-------------------------клавиатуры миню конкретной даты, взятой из календаря----------------------------------------------------


# Инлай клавиатура для меню admin, где перечислены предметы группы
def create_admin_menu_date_keyboard(user_id, date) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['buttons']
    # Получаем год, месяц, день
    year, month, day = date.split('_')[-3:]
    date = f"{year}-{month}-{day}"
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем все предметы группы, где есть домашние задание на конкретную дату
    data = get_subject_with_homework_for_date(group_id, date)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с предметами в клавиатуру
    if data:
        kb_builder.row(*[InlineKeyboardButton(text=name,
                                              callback_data=f'admin_date_subject_id_{subject_id}_{date}') for name, subject_id, message in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['no_homework'], callback_data='something'))
    # Разделитьель предметов от кнопок
    kb_builder.row(InlineKeyboardButton(text=LEXICON()['general']['fence'], callback_data="fence"))
    # Генерируем остальные кнопки
    kb_builder.row(InlineKeyboardButton(text=LEXICON()['general']['menu_date']['get_all_hw'], callback_data='get_all_hw'), width=1)
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=f"{button}_{year}_{month}_{day}") for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


# Инлай клавиатура для меню admin, где перечислены предметы группы для добавления дз
def create_FSM_all_subjects_keyboard(user_id) -> InlineKeyboardMarkup:
    # Получаем group_id
    group_id = get_user(user_id)[-1][-1]
    # Получаем все предметы группы
    data = get_all_subjects_by_group(group_id)
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Добавляем кнопки с предметами в клавиатуру
    if data:
        kb_builder.row(*[InlineKeyboardButton(text=f"{name}",
                                              callback_data=f'admin_FSM_subject_id_{subject_id}') for subject_id, name, group_id in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=LEXICON()['admin']['admin_menu_subjects']['no_subjects'], callback_data='something'))

    return kb_builder.as_markup()