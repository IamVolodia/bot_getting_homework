from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models.functions import get_homework_for_year_month_and_group, get_user
from aiogram.types import CallbackQuery
import calendar


# Инлай клавиатура для меню admin - календарь
def create_calendar_keyboard(status, date, callback: CallbackQuery) -> InlineKeyboardMarkup:
    # Плучаем нужынй год и месяц из даты
    if type(date) == str:
        year, month, day = map(int, date.split("_")[-3:])
    else:
        year, month = date.year, date.month
    # Получаем номер дня недели с которого начинается месяц и дней в месяце
    weekday, days = calendar.monthrange(year, month)
    # Создаем два списка с перечислением месяцев и дней недели для дальнейшего форматировнаия текста
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    # Создаем клавиатуру
    kb_builder = InlineKeyboardBuilder()
    # Создаем инлайн кнопку, которая будет показывать текущий месяц и год, реакция на нажатие будет отсутствовать
    kb_builder.row(InlineKeyboardButton(text=f"{months[month-1]} {year}", callback_data="something"), width=1)
    # Создаем инлайн кнопку, которая будет перечеслять дни недели, реакция на нажатие будет отсутствовать
    kb_builder.row(*[InlineKeyboardButton(text=i, callback_data="something") for i in weekdays], width=7)
    # Заполняем пустотами лист до того момента, когда будет первое число месяца
    week = [" " for i in range(weekday)]
    # получаем id группы
    group_id = get_user(callback.from_user.id)[-1][-1]
    # Получаем все домашние задания за определенный год и месяц
    days_with_homework = [int(i[1].split("-")[-1]) for i in get_homework_for_year_month_and_group(f"{year}-{month}", group_id)]
    # Запускаем цикл с днями месяца
    for i in range(1, days + 1):
        # Делаем проверку на заполненность недели датами и генерируем кнопк из списка
        if len(week) == 7:
            kb_builder.row(*[InlineKeyboardButton(text=f"📚{str(day)}", callback_data=f'{status}_date_{year}_{month}_{day}') if day in days_with_homework 
                            else InlineKeyboardButton(text=f"{str(day)}", callback_data=f'{status}_date_{year}_{month}_{day}')
                            for day in week], width=7)
            # Обнуляем счетчик дат
            week = []
        week.append(i)
    # Если после прошедшего цикла у нас остался заполненный датами список, то генерируем кнопки,
    # если нет, то добиваем пустотами до семи и так же генерируем
    if len(week) == 7:
        kb_builder.row(*[InlineKeyboardButton(text=f"📚{str(day)}", callback_data=f'{status}_date_{year}_{month}_{day}') if day in days_with_homework 
                            else InlineKeyboardButton(text=f"{str(day)}", callback_data=f'{status}_date_{year}_{month}_{day}')
                            for day in week], width=7)
    elif 1 <= len(week) < 7:
        for i in range(7):
            if len(week) == 7:
                break
            week.append(" ")
        kb_builder.row(*[InlineKeyboardButton(text=f"📚{str(day)}", callback_data=f'{status}_date_{year}_{month}_{day}') if day in days_with_homework 
                            else InlineKeyboardButton(text=f"{str(day)}", callback_data=f'{status}_date_{year}_{month}_{day}')
                            for day in week], width=7)

    # Делаем callback кнопки Назад, в зависимости от того, кто пользуется клавиутарой
    if status == 'admin':
        back = 'admin_back_to_menu'
    else:
        back = 'user_back_to_menu'

    # Здесь мы создаем callback для кнопки вперед и назад переключения месяцев календаря
    if month == 1:
        backward = f'{status}_calendar_another_month_{year - 1}_{12}_{1}'
        forward = f'{status}_calendar_another_month_{year}_{month + 1}_{1}'
    elif month == 12:
        forward = f'{status}_calendar_another_month_{year + 1}_{1}_{1}'
        backward = f'{status}_calendar_another_month_{year}_{month - 1}_{1}'
    else:
        forward = f'{status}_calendar_another_month_{year}_{month + 1}_{1}'
        backward = f'{status}_calendar_another_month_{year}_{month - 1}_{1}'

    # Добавляем кнопки и возвращаем инлайн клавиатуру
    kb_builder.row(InlineKeyboardButton(text='<<', callback_data=backward),
                   InlineKeyboardButton(text="Назад", callback_data=back),
                   InlineKeyboardButton(text='>>', callback_data=forward), width=3)
    return kb_builder.as_markup()
