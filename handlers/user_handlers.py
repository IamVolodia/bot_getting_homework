from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.user_kb import *
from keyboards.admin_kb import create_start_keyboard_if_admin
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_user_to_database, add_group_to_database
from models.functions import add_user_to_group, add_admin, get_group_by_name
from aiogram.fsm.state import default_state
from filters.filters import IsUserNotHaveGroup, IsFSMGroupName, IsGroupByThatName
from FSM.user_fsm import FSMCreatGroup, FSMJoinGroup

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
    # Добавление пользователя в базу данных
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
