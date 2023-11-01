from aiogram import F, Router, Bot
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.admin_kb import *
from keyboards.calendar_kb import *
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_group_to_database, add_user_to_database, add_subject_to_database
from models.functions import del_admin, add_admin, del_group, del_user_from_group, del_subject, get_subject_by_name
from filters.filters import (IsUserHaveStatusAdmin, IsAddStatusAdmin, IsDelStatusAdmin,
                             IsDelUserFromGroup, IsDelGroup, IsDelSubjectFromGroup,
                             IsFSMSubjectName, IsSubjectFromGroup, IsRightDate,
                             IsGroupHaveSubject, IsAddHomework)
from aiogram.fsm.state import default_state
from FSM.admin_fsm import *
from utils.utils import save_message_to_database

router = Router()
router.message.filter(IsUserHaveStatusAdmin())


# Хендлер на комманду старт, если у тебя права админа
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command_if_admin(message: Message):
    # Добавление пользователя в базу данных
    await add_user_to_database(message.from_user.id, message.from_user.username)
    await message.answer(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())


#---------------------инлайн клавиатура с участниками группы----------------------------------


# Меню админа со списком пользователей группы
@router.callback_query(F.data == 'admin_users', StateFilter(default_state))
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['text_menu'],
                         reply_markup=create_admin_menu_users_keyboard(callback.from_user.id))

#---------------------назначение прав админа---------------------------------------------------


# Меню назначения прав админа пользователю группы
@router.callback_query(F.data == 'admin_add_admin', StateFilter(default_state))
async def process_admin_add_admin_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_add_admin']['text_menu'],
                         reply_markup=create_admin_menu_add_admin_keyboard(callback.from_user.id))


# Назначение прав админа юзеру
@router.callback_query(IsAddStatusAdmin(), StateFilter(default_state))
async def process_add_status_admin_press(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id == int(callback.data.split("_")[-1]):
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_add_admin']['add_yourself'], show_alert=True)
    elif get_user(int(callback.data.split("_")[-1]))[0][-2] == 1:
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_add_admin']['add_admin'], show_alert=True)
    else:
        add_admin(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_add_admin']['text_menu'],
                         reply_markup=create_admin_menu_add_admin_keyboard(callback.from_user.id))


#---------------------удаление прав админа---------------------------------------------------


# Меню удаления статуса админа у пользователя группы
@router.callback_query(F.data == 'admin_del_admin', StateFilter(default_state))
async def process_admin_del_admin_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['text_menu'],
                         reply_markup=create_admin_menu_del_admin_keyboard(callback.from_user.id))


# Удаление прав админа
@router.callback_query(IsDelStatusAdmin(), StateFilter(default_state))
async def process_add_status_admin_press(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id == int(callback.data.split("_")[-1]):
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['del_yourself'], show_alert=True)
    elif get_user(int(callback.data.split("_")[-1]))[0][-2] == 0:
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['del_user'], show_alert=True)
    else:
        del_admin(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['text_menu'],
                         reply_markup=create_admin_menu_del_admin_keyboard(callback.from_user.id))


#---------------------удаление пользователя---------------------------------------------------


# Меню удаления пользователя из группы
@router.callback_query(F.data == 'admin_del_user', StateFilter(default_state))
async def process_admin_del_user_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['text_menu'],
                         reply_markup=create_admin_menu_del_user_keyboard(callback.from_user.id))


# Удаление пользователя из группы
@router.callback_query(IsDelUserFromGroup(), StateFilter(default_state))
async def process_del_user_press(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id == int(callback.data.split("_")[-1]):
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['del_yourself'], show_alert=True)
    else:
        del_user_from_group(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['text_menu'],
                         reply_markup=create_admin_menu_del_user_keyboard(callback.from_user.id))


#---------------------хендлеры по нажатию кнопки 'Удаление группы'--------------------------------------------------------


# Меню удаления статуса админа у пользователя группы
@router.callback_query(F.data == 'admin_del_group', StateFilter(default_state))
async def process_admin_del_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_del_group']['text_menu'],
                         reply_markup=create_admin_menu_del_group_keyboard(callback.from_user.id))


# Меню удаления статуса админа у пользователя группы
@router.callback_query(F.data == 'admin_del_group_two', StateFilter(default_state))
async def process_admin_del_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_del_group']['admin_menu_del_group_two']['text_menu'],
                         reply_markup=create_admin_menu_del_group_two_keyboard(callback.from_user.id))


# Удаление группы
@router.callback_query(IsDelGroup(), StateFilter(default_state))
async def process_del_user_press(callback: CallbackQuery, state: FSMContext):
    group_id = get_user(callback.from_user.id)[-1][-1]
    del_group(group_id)
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_del_group']['admin_menu_del_group_two']['group_deleted'])



#---------------------инлайн клавиатура с предметами группы группы-------------------------------------------


# Меню админа со списком предметов группы
@router.callback_query(F.data == 'admin_subjects', StateFilter(default_state))
async def process_admin_subjects_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['text_menu'],
                         reply_markup=create_admin_menu_subjects_keyboard(callback.from_user.id))


#---------------------инлайн клавиатура с предметами группы к удалению----------------------------------


# Меню админа со списком предметов группы к удалению
@router.callback_query(F.data == 'admin_del_subject', StateFilter(default_state))
async def process_admin_del_subject_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['admin_menu_del_subject']['text_menu'],
                         reply_markup=create_admin_menu_del_subjects_keyboard(callback.from_user.id))


# Удаление предмета из группы
@router.callback_query(IsDelSubjectFromGroup(), StateFilter(default_state))
async def process_del_subject_press(callback: CallbackQuery, state: FSMContext):
    del_subject(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['admin_menu_del_subject']['text_menu'],
                         reply_markup=create_admin_menu_del_subjects_keyboard(callback.from_user.id))



#---------------------------------машина состояний по созданию предмета----------------------------------------------------


# Хендлер на запуск машины состояний по созданию предмета
@router.callback_query(F.data == 'admin_add_subject', StateFilter(default_state))
async def process_admin_add_subject_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['FSM_creat_subject']['entering_name'])
    await state.set_state(FSMCreatSubject.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное название предмета
@router.message(StateFilter(FSMCreatSubject.fill_name), IsFSMSubjectName())
async def process_admin_name_subject_sent(message: Message, state: FSMContext):
    group_id = get_user(message.from_user.id)[-1][-1]
    await add_subject_to_database(message.text, group_id)
    # Завершаем машину состояний
    await state.clear()
    # Вызываем меню предметов
    await message.answer(text=LEXICON()['admin']['admin_menu_subjects']['text_menu'],
                         reply_markup=create_admin_menu_subjects_keyboard(message.from_user.id))


# Этот хэндлер будет срабатывать, если во время ввода названия предмета
# будет введено что-то некорректное
@router.message(StateFilter(FSMCreatSubject.fill_name))
async def warning_admin_name_subject(message: Message):
    await message.answer(text=LEXICON()['admin']['admin_menu_subjects']['FSM_creat_subject']['name_entry_error'])



#---------------------------------открытие календаря в главном меню------------------------------------------------------------


# Меню админа - календарь
@router.callback_query(F.data == 'admin_calendar', StateFilter(default_state))
async def process_admin_calendar_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['text_menu'],
                         reply_markup=create_calendar_keyboard(status="admin", date=callback.message.date))


# Меню админа - календарь - другой месяц
@router.callback_query(F.data.startswith('admin_calendar_another_month_'), StateFilter(default_state))
async def process_admin_calendar_another_month_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['text_menu'],
                         reply_markup=create_calendar_keyboard(status="admin", date=callback.data))


# Меню админа - календарь - конкретная дата
@router.callback_query(IsRightDate(), StateFilter(default_state))
async def process_admin_calendar_date_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['text_menu'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=callback.from_user.id, date=callback.data))


#----------------------открытие календаря в главном меню - запуск машины состояний по добавлению дз-----------------------------


# Хендлер на запуск машины состояний по добавлению дз
@router.callback_query(IsAddHomework(), StateFilter(default_state), IsGroupHaveSubject())
async def process_admin_add_homework_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['choice_subject'],
                                     reply_markup=create_FSM_all_subjects_keyboard(callback.from_user.id))
    await state.update_data(date='-'.join(callback.data.split("_")[-3:]))
    await state.set_state(FSMAddHomework.fill_subject_name)


# Если у группы нет предметов, то будет отправлено соответсвующее собщение и машина состояний не будет запущена
@router.callback_query(IsAddHomework(), StateFilter(default_state))
async def process_admin_add_homework_wrong_press(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['group_havent_subjects'],
                                     show_alert=True)


# Этот хэндлер будет срабатывать на название предмета
@router.callback_query(StateFilter(FSMAddHomework.fill_subject_name))
async def process_admin_name_subject_for_homework_sent(callback: CallbackQuery, state: FSMContext):
    subject_id = callback.data.split('_')[-1]
    await state.update_data(subject_id=subject_id)
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['sent_homework'])
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMAddHomework.fill_message)


# Этот хэндлер будет срабатывать на отправленое сообщнение и добавлять его в базу данных
@router.message(StateFilter(FSMAddHomework.fill_message))
async def process_admin_message_save_to_db(message: Message, state: FSMContext):
    # Получаем данные из машины состояний
    data = await state.get_data()
    # Добавляем домашнее задание в базу данных
    await save_message_to_database(date=data["date"], subject_id=data["subject_id"], message=message)
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['successful_add'])
    await message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['text_menu'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=message.from_user.id, date=data["date"].replece('-', '_')))


#---------------------хендлеры по нажатию кнопки 'назад'--------------------------------------------------------


# Кнопка возвращение в меню админа
@router.callback_query(F.data == 'admin_back_to_menu', StateFilter(default_state))
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())


# Кнопка возвращения в меню со списком пользователей группы
@router.callback_query(F.data == 'admin_back_to_menu_users', StateFilter(default_state))
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['text_menu'],
                         reply_markup=create_admin_menu_users_keyboard(callback.from_user.id))


# Кнопка возвращения в меню со списком предметов группы
@router.callback_query(F.data == 'admin_back_to_menu_subject', StateFilter(default_state))
async def process_admin_subjects_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['text_menu'],
                         reply_markup=create_admin_menu_subjects_keyboard(callback.from_user.id))