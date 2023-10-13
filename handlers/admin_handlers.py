from aiogram import F, Router
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.admin_kb import *
from keyboards.calendar_kb import *
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_group_to_database, add_user_to_database, add_subject_to_database
from models.functions import del_admin, add_admin, del_group, del_user_from_group, del_subject
from filters.filters import (IsUserHaveStatusAdmin, IsAddStatusAdmin, IsDelStatusAdmin,
                             IsDelUserFromGroup, IsDelGroup, IsDelSubjectFromGroup,
                             IsFSMSubjectName, IsSubjectFromGroup)
from aiogram.fsm.state import default_state
from FSM.admin_fsm import FSMCreatSubject
import _pickle as cPickle

router = Router()


# Хендлер на комманду старт, если у тебя права админа
@router.message(CommandStart(), StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_start_command_if_admin(message: Message):
    # Добавление пользователя в базу данных
    await add_user_to_database(message.from_user.id, message.from_user.username)
    await message.answer(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())


#---------------------инлайн клавиатура с участниками группы----------------------------------


# Меню админа со списком пользователей группы
@router.callback_query(F.data == 'admin_users', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['text_menu'],
                         reply_markup=create_admin_menu_users_keyboard(callback.from_user.id))

#---------------------назначение прав админа---------------------------------------------------


# Меню назначения прав админа пользователю группы
@router.callback_query(F.data == 'admin_add_admin', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_add_admin_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_add_admin']['text_menu'],
                         reply_markup=create_admin_menu_add_admin_keyboard(callback.from_user.id))


# Назначение прав админа юзеру
@router.callback_query(IsAddStatusAdmin(), StateFilter(default_state), IsUserHaveStatusAdmin())
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
@router.callback_query(F.data == 'admin_del_admin', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_del_admin_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['text_menu'],
                         reply_markup=create_admin_menu_del_admin_keyboard(callback.from_user.id))


# Удаление прав админа
@router.callback_query(IsDelStatusAdmin(), StateFilter(default_state), IsUserHaveStatusAdmin())
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
@router.callback_query(F.data == 'admin_del_user', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_del_user_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['text_menu'],
                         reply_markup=create_admin_menu_del_user_keyboard(callback.from_user.id))


# Удаление пользователя из группы
@router.callback_query(IsDelUserFromGroup(), StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_del_user_press(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id == int(callback.data.split("_")[-1]):
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['del_yourself'], show_alert=True)
    else:
        del_user_from_group(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['text_menu'],
                         reply_markup=create_admin_menu_del_user_keyboard(callback.from_user.id))


#---------------------хендлеры по нажатию кнопки 'Удаление группы'--------------------------------------------------------


# Меню удаления статуса админа у пользователя группы
@router.callback_query(F.data == 'admin_del_group', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_del_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_del_group']['text_menu'],
                         reply_markup=create_admin_menu_del_group_keyboard(callback.from_user.id))


# Меню удаления статуса админа у пользователя группы
@router.callback_query(F.data == 'admin_del_group_two', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_del_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_del_group']['admin_menu_del_group_two']['text_menu'],
                         reply_markup=create_admin_menu_del_group_two_keyboard(callback.from_user.id))


# Удаление группы
@router.callback_query(IsDelGroup(), StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_del_user_press(callback: CallbackQuery, state: FSMContext):
    group_id = get_user(callback.from_user.id)[-1][-1]
    del_group(group_id)
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_del_group']['admin_menu_del_group_two']['group_deleted'])



#---------------------инлайн клавиатура с предметами группы группы-------------------------------------------


# Меню админа со списком предметов группы
@router.callback_query(F.data == 'admin_subjects', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_subjects_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['text_menu'],
                         reply_markup=create_admin_menu_subjects_keyboard(callback.from_user.id))


#---------------------инлайн клавиатура с предметами группы к удалению----------------------------------


# Меню админа со списком предметов группы к удалению
@router.callback_query(F.data == 'admin_del_subject', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_del_subject_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['admin_menu_del_subject']['text_menu'],
                         reply_markup=create_admin_menu_del_subjects_keyboard(callback.from_user.id))


# Удаление предмета из группы
@router.callback_query(IsDelSubjectFromGroup(), StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_del_subject_press(callback: CallbackQuery, state: FSMContext):
    del_subject(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['admin_menu_del_subject']['text_menu'],
                         reply_markup=create_admin_menu_del_subjects_keyboard(callback.from_user.id))



#---------------------------------машина состояний по созданию предмета----------------------------------------------------


# Хендлер на запуск машины состояний по созданию предмета
@router.callback_query(F.data == 'admin_add_subject', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_add_subject_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['FSM_creat_subject']['entering_name'])
    await state.set_state(FSMCreatSubject.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное название предмета
@router.message(StateFilter(FSMCreatSubject.fill_name), IsFSMSubjectName(), IsUserHaveStatusAdmin())
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
@router.message(StateFilter(FSMCreatSubject.fill_name), IsUserHaveStatusAdmin())
async def warning_admin_name_subject(message: Message):
    await message.answer(text=LEXICON()['admin']['admin_menu_subjects']['FSM_creat_subject']['name_entry_error'])



#---------------------------------меню конкретного предмета, календарь------------------------------------------


# Меню админа - меню предметов - предмет
@router.callback_query(F.data == 'admin_calendar', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_calendar_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['text_menu'],
                         reply_markup=create_calendar_keyboard(status="admin"))




#---------------------хендлеры по нажатию кнопки 'назад'--------------------------------------------------------


# Кнопка возвращение в меню админа
@router.callback_query(F.data == 'admin_back_to_menu', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())


# Кнопка возвращения в меню со списком пользователей группы
@router.callback_query(F.data == 'admin_back_to_menu_users', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['text_menu'],
                         reply_markup=create_admin_menu_users_keyboard(callback.from_user.id))


# Кнопка возвращения в меню со списком предметов группы
@router.callback_query(F.data == 'admin_back_to_menu_subject', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_subjects_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['text_menu'],
                         reply_markup=create_admin_menu_subjects_keyboard(callback.from_user.id))