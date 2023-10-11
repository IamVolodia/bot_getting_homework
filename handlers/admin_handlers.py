from aiogram import F, Router
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.admin_kb import *
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_group_to_database, add_user_to_database
from models.functions import del_admin, add_admin, del_group, del_user_from_group
from filters.filters import IsUserHaveStatusAdmin, IsAddStatusAdmin, IsDelStatusAdmin, IsDelUserFromGroup, IsDelGroup
from aiogram.fsm.state import default_state
from FSM.superadmin_fsm import FSMAssignment, FSMAddGroup
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


# Меню удаления статуса админа у пользователя группы
@router.callback_query(F.data == 'admin_del_user', StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_admin_del_user_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['text_menu'],
                         reply_markup=create_admin_menu_del_user_keyboard(callback.from_user.id))


# Удаление прав админа
@router.callback_query(IsDelUserFromGroup(), StateFilter(default_state), IsUserHaveStatusAdmin())
async def process_del_user_press(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id == int(callback.data.split("_")[-1]):
        await callback.answer(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_user']['del_yourself'], show_alert=True)
    else:
        del_user_from_group(int(callback.data.split("_")[-1]))
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['admin_menu_del_admin']['text_menu'],
                         reply_markup=create_admin_menu_del_admin_keyboard(callback.from_user.id))


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

#--------------------------------------------------------------------------------------------------------------------



# # Добавление админа в группу
# @router.callback_query(F.data == 'admin_add_admin', StateFilter(default_state))
# async def process_add_admin_press(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['add_admin_text_menu'])
#     await state.set_state(FSMAssignment.fill_new_admin_id)


# # Этот хэндлер будет срабатывать, если введено корректное id
# # и переводить в состояние ожидания ввода возраста
# @router.message(StateFilter(FSMAssignment.fill_new_admin_id), IsFSMRightID())
# async def process_user_id_sent(message: Message, state: FSMContext):
#     # Даем права админа пользователю
#     add_admin(message.text)
#     await message.answer(text=LEXICON()['superadmin']['menu_admins']['true_id_FSM'])
#     # Завершаем машину состояний
#     await state.clear()


# # Этот хэндлер будет срабатывать, если во время ввода id
# # будет введено что-то некорректное
# @router.message(StateFilter(FSMAssignment.fill_new_admin_id))
# async def warning_not_user_id(message: Message):
#     await message.answer(text=LEXICON()['superadmin']['menu_admins']['false_id_FSM'])