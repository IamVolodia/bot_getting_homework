from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from models.functions import get_user_group, get_date_group, get_user, get_all_users_by_group, get_all_subjects_by_group
from datetime import datetime, timedelta
import calendar


# Инлай клавиатура для меню admin - календарь
def create_calendar_keyboard(status) -> InlineKeyboardMarkup:
    # Получаем текущую дату
    today = datetime.now().date()
    year, month, day_ = today.year, today.month, today.day
    #
    weekday, days = calendar.monthrange(year, month)
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=f"{months[month-1]} {year}", callback_data="something"), width=1)
    kb_builder.row(*[InlineKeyboardButton(text=i, callback_data="something") for i in weekdays], width=7)
    week = [" " for i in range(weekday)]
    for i in range(1, days):
        if len(week) == 7:
            kb_builder.row(*[InlineKeyboardButton(text=str(day),
                                                  callback_data=f'{status}_date_{year}_{month}_{day}') for day in week], width=7)
            week = []
        week.append(i)
    if len(week) == 7:
        kb_builder.row(*[InlineKeyboardButton(text=str(day),
                                              callback_data=f'{status}_date_{year}_{month}_{day}') for day in week], width=7)
    elif 1 <= len(week) < 7:
        for i in range(7):
            if len(week) == 7:
                break
            week.append(" ")
        kb_builder.row(*[InlineKeyboardButton(text=str(day),
                                              callback_data=f'{status}_date_{year}_{month}_{day}') for day in week], width=7)
    if status == 'admin':
        back = 'admin_back_to_menu'
    else:
        back = 'user_back_to_menu'

    if month == 1:
        forward = f'{status}_{year - 1}_{12}'
    elif month == 12:
        backward = f'{status}_{year + 1}_{1}'
    else:
        forward = f'{status}_{year}_{month + 1}'
        backward = f'{status}_{year}_{month - 1}'

    kb_builder.row(InlineKeyboardButton(text='<<', callback_data=backward),
                   InlineKeyboardButton(text="Назад", callback_data=back),
                   InlineKeyboardButton(text='>>', callback_data=forward), width=3)

    return kb_builder.as_markup()
