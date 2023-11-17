from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.user_kb import *
from keyboards.admin_kb import create_start_keyboard_if_admin
from lexicon.lexicon import LEXICON
from models.methods import add_user_to_database, add_group_to_database
from models.functions import add_user_to_group, add_admin, get_group_by_name, get_subject_by_id, get_subject_with_homework_for_date, del_user_from_group
from aiogram.fsm.state import default_state
from filters.filters import IsUserNotHaveGroup, IsFSMGroupName, IsGroupByThatName, IsRightDateForUser, IsUserSubjectFromCalendar
from FSM.user_fsm import FSMCreatGroup, FSMJoinGroup
from keyboards.calendar_kb import create_calendar_keyboard
from utils.message_converter import get_homeworks_from_database
from aiogram.exceptions import TelegramBadRequest


router = Router()

# Хендлер на комманду старт, если нет группы
@router.message(CommandStart(), StateFilter(default_state), IsUserNotHaveGroup())
async def process_start_command_if_not_group(message: Message):
    # Добавление пользователя в базу данных
    await add_user_to_database(message.from_user.id, message.from_user.username)
    await message.answer(text=LEXICON()['user']['havent_group']['text_menu'],
                         reply_markup=create_start_keyboard_if_not_group())


# Хендлер на комманду старт, если есть группа
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON()['user']['have_group']['text_menu'],
                         reply_markup=create_start_keyboard())


#---------------------------------машина состояний по созданию группы----------------------------------------------------


# Хендлер на запуск машины состояний по созданию группы
@router.callback_query(F.data == 'user_creat_group', StateFilter(default_state))
async def process_user_create_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['havent_group']['FSM_creat_group']['entering_name'])
    await state.set_state(FSMCreatGroup.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное название группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMCreatGroup.fill_name), IsFSMGroupName())
async def process_user_name_group_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON()['user']['havent_group']['FSM_creat_group']['entering_password'])
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMCreatGroup.fill_password)


# Этот хэндлер будет срабатывать, если во время ввода названия группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMCreatGroup.fill_name))
async def warning_user_not_name_group(message: Message):
    await message.answer(text=LEXICON()['user']['havent_group']['FSM_creat_group']['name_entry_error'])


# Этот хэндлер будет срабатывать, если введен корректный пароль группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMCreatGroup.fill_password), lambda x: 1 <= len(x.text) <= 10)
async def process_user_password_group_sent(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    # Добавляем в бд группу
    data = await state.get_data()
    await add_group_to_database(name=data['name'], password=data['password'])
    # Добавляем пользователя в группу
    add_user_to_group(message.from_user.id, group_name=data['name'])
    add_admin(message.from_user.id)
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())


# Этот хэндлер будет срабатывать, если во время ввода пароля группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMCreatGroup.fill_password))
async def warning_user_not_password_group(message: Message):
    await message.answer(text=LEXICON()['user']['havent_group']['FSM_creat_group']['password_entry_error'])



#---------------------------------машина состояний по присоеденению к группе----------------------------------------------------


# Хендлер на запуск машины состояний по присоеденению к группе
@router.callback_query(F.data == 'user_join_group', StateFilter(default_state))
async def process_user_join_to_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['havent_group']['FSM_join_group']['entering_name'])
    await state.set_state(FSMJoinGroup.fill_name)


# Этот хэндлер будет срабатывать, если введено существующее название группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMJoinGroup.fill_name), IsGroupByThatName())
async def process_user_join_name_group_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON()['user']['havent_group']['FSM_join_group']['entering_password'])
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMJoinGroup.fill_password)


# Этот хэндлер будет срабатывать, если во время ввода названия группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMJoinGroup.fill_name))
async def warning_user_join_not_name_group(message: Message):
    await message.answer(text=LEXICON()['user']['havent_group']['FSM_join_group']['name_entry_error'])


# Этот хэндлер будет срабатывать на ввод пароля от группы
@router.message(StateFilter(FSMJoinGroup.fill_password))
async def process_user_join_password_group_sent(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if get_group_by_name(name=data['name'])[0][-1] == data['password']:
        # Добавляем пользователя в группу
        add_user_to_group(message.from_user.id, group_name=data['name'])
        # Завершаем машину состояний
        await state.clear()
        await message.answer(text=LEXICON()['user']['have_group']['text_menu'],
                            reply_markup=create_start_keyboard())
    else:
        await message.answer(text=LEXICON()['user']['havent_group']['FSM_join_group']['password_entry_error'])


#---------------------------------открытие календаря в главном меню------------------------------------------------------------


# Меню пользователя - календарь
@router.callback_query(F.data == 'user_calendar', StateFilter(default_state))
async def process_user_calendar_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['user_menu_calendar']['text_menu'],
                         reply_markup=create_calendar_keyboard(status="user", date=callback.message.date, callback=callback))


# Меню пользователя - календарь - другой месяц
@router.callback_query(F.data.startswith('user_calendar_another_month_'), StateFilter(default_state))
async def process_user_calendar_another_month_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['user_menu_calendar']['text_menu'],
                         reply_markup=create_calendar_keyboard(status="user", date=callback.data, callback=callback))


# Меню пользователя - календарь - конкретная дата
@router.callback_query(IsRightDateForUser(), StateFilter(default_state))
async def process_user_calendar_date_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['user_menu_calendar']['user_menu_date']['text_menu'],
                         reply_markup=create_user_menu_date_keyboard(user_id=callback.from_user.id, date=callback.data))


#---------------------------------полученеи домашнего задания по конкретному предмету----------------------------------------------


# Хендлер на конкретный предмет за определенную дату
@router.callback_query(IsUserSubjectFromCalendar(), StateFilter(default_state))
async def process_user_subject_in_date_press(callback: CallbackQuery):
    # Получаем id предмета и дату
    subject_id, date = callback.data.split("_")[-2:]
    # Плучаем название предмета по id
    subject_name = get_subject_by_id(subject_id)
    # Отправляем сообщением название предмета, по которому необходимо дз
    await callback.message.answer(text=f"Домашние задания по {subject_name[0][1]} за {date}:")
    # Отправка сообщение всей домашней работы по выбраному предмету за эту дату
    await get_homeworks_from_database(date=date, subject_id=subject_id, callback=callback)
    await callback.message.answer(text=LEXICON()['user']['user_menu_calendar']['user_menu_date']['text_menu'],
                         reply_markup=create_user_menu_date_keyboard(user_id=callback.from_user.id, date=date.replace('-', '_')))


# Получение всех домашних заданий за определенную дату
@router.callback_query(F.data.startswith('user_get_all_homework'), StateFilter(default_state))
async def process_user_subject_in_date_press(callback: CallbackQuery):
    # Получаем id группы
    group_id = get_user(callback.from_user.id)[-1][-1]
    # Получаем дату
    year, month, day = callback.data.split('_')[-3:]
    date = f"{year}-{month}-{day}"
    # Плучаем данные всех предметов, у которых есть домашнее задание на эту дату
    subjects = get_subject_with_homework_for_date(group_id, date)
    for subject_name, subject_id in subjects:
        # Отправляем сообщением название предмета, по которому необходимо дз
        await callback.message.answer(text=f"Домашние задания по {subject_name} за {date}:")
        # Отправка сообщение всей домашней работы по выбраному предмету за эту дату
        await get_homeworks_from_database(date=date, subject_id=subject_id, callback=callback)
    await callback.message.answer(text=LEXICON()['user']['user_menu_calendar']['user_menu_date']['text_menu'],
                         reply_markup=create_user_menu_date_keyboard(user_id=callback.from_user.id, date=date.replace('-', '_')))
    

#---------------------------------полученеи домашнего задания на завтра-------------------------------------------------------------


# Хендлер на получение домашнего задания на завтра
@router.callback_query(F.data.startswith('user_today'), StateFilter(default_state))
async def process_user_homework_today_press(callback: CallbackQuery):
    # Получаем id группы
    group_id = get_user(callback.from_user.id)[-1][-1]
    # Получаем дату
    date = callback.message.date
    date = f"{date.year}-{date.month}-{date.day + 1}"
    # Плучаем данные всех предметов, у которых есть домашнее задание на эту дату
    subjects = get_subject_with_homework_for_date(group_id, date)
    if subjects:
        for subject_name, subject_id in subjects:
            # Отправляем сообщением название предмета, по которому необходимо дз
            await callback.message.answer(text=f"Домашние задания по {subject_name} за {date}:")
            # Отправка сообщение всей домашней работы по выбраному предмету за эту дату
            await get_homeworks_from_database(date=date, subject_id=subject_id, callback=callback)
        await callback.message.answer(text=LEXICON()['user']['have_group']['text_menu'],
                            reply_markup=create_start_keyboard())
    await callback.answer(text=LEXICON()['user']['have_group']['no_homework_today'],
                          show_alert=True)
    

#---------------------------------покинуть группу-------------------------------------------------------------


# Хендлер на кнопку покинуть группу
@router.callback_query(F.data == 'user_leave_group', StateFilter(default_state))
async def process_user_leave_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['have_group']['user_question_leave_group']['text_menu'],
                                     reply_markup=create_user_leave_group_keyboard())


# Хендлер на кнопку покинуть группу
@router.callback_query(F.data == 'user_yes_leave_group', StateFilter(default_state))
async def process_user_left_group_press(callback: CallbackQuery, state: FSMContext):
    del_user_from_group(callback.from_user.id)
    await callback.message.edit_text(text=LEXICON()['user']['have_group']['user_question_leave_group']['user_left_group'],
                                     reply_markup=create_start_keyboard_if_not_group()) 

    

#---------------------------------кнопки назад-------------------------------------------------------------


# Хендлер на запуск машины состояний по созданию группы
@router.callback_query(F.data == 'user_back_to_menu', StateFilter(default_state))
async def process_user_back_to_menu_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['user']['have_group']['text_menu'],
                         reply_markup=create_start_keyboard())