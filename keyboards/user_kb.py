from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_user, get_subject_with_homework_for_date


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


# Инлай клавиатура для меню user, где перечислены предметы группы
def create_user_menu_date_keyboard(user_id, date) -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['user']['user_menu_calendar']['user_menu_date']['buttons']
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
                                              callback_data=f'user_date_subject_id_{subject_id}_{date}') for name, subject_id in data], width=1)
    else:
        kb_builder.row(InlineKeyboardButton(text=LEXICON()['user']['user_menu_calendar']['user_menu_date']['no_homework'], callback_data='something'))
    # Разделитьель предметов от кнопок
    kb_builder.row(InlineKeyboardButton(text=LEXICON()['general']['fence'], callback_data="fence"))
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=f"{button}_{year}_{month}_{day}") for button, text in buttons.items()], width=1)

    return kb_builder.as_markup()


# Инлай клавиатура для вызода из группы
def create_user_leave_group_keyboard() -> InlineKeyboardMarkup:
    # Получаем кнопки меню
    buttons = LEXICON()['user']['have_group']['user_question_leave_group']['buttons']
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Генерируем остальные кнопки
    kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=button) for button, text in buttons.items()], width=2)

    return kb_builder.as_markup()