from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.superadmin_kb import *
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.methods import add_group_to_database
from models.functions import del_admin, add_admin, del_group
from filters.filters import IsDelAdminCallbackData, IsFSMRightID, IsDelGroupCallbackData, IsFSMGroupName, IsGroupCallbackData
from aiogram.fsm.state import default_state
from FSM.superadmin_fsm import FSMAssignment, FSMAddGroup
import _pickle as cPickle


router = Router()


# Вызов инлайн клавиатуры суперадмина
@router.message(Command(commands='superadmin'), StateFilter(default_state))
async def process_superadmin_command(message: Message):
    if message.from_user.id in load_config().tg_bot.superadmin_ids:
        await message.answer(text=LEXICON()['superadmin']['text_menu'],
                             reply_markup=create_superadmin_keyboard())
    else:
        await message.answer(text=LEXICON()['superadmin']['no_rights'])


# ----------------------команда отмены машины состояний--------------------------------------------------------------------


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON()['general']['cancel_FSM_False'])


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON()['general']['cancel_FSM'])
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# ----------------------мену по редактированию групп--------------------------------------------------------------------


# Вызов инлайн клавиатуры со списком групп, при нажатии кнопки группы
@router.callback_query(F.data == 'groups', StateFilter(default_state))
async def process_groups_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_groups']['text_menu'],
                                         reply_markup=create_groups_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# Вызов инлайн клавиатуры со списком групп к их удалению, при нажатии кнопки Удалить группу
@router.callback_query(F.data == 'delete_group', StateFilter(default_state))
async def process_delete_group_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_groups']['delete_group_text_menu'],
                                         reply_markup=create_delete_groups_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# Удаление группы
@router.callback_query(IsDelGroupCallbackData(), StateFilter(default_state))
async def process_dell_group_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        del_group(int(callback.data.split("_")[-1]))
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_groups']['delete_group_text_menu'],
                                         reply_markup=create_delete_groups_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()



# ----------------------запуск машины состояний по добавлению группы--------------------------------------------------------------------


# Добавление группы
@router.callback_query(F.data == 'add_group', StateFilter(default_state))
async def process_add_group_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['superadmin']['menu_groups']['add_group_name_text_menu'])
    await state.set_state(FSMAddGroup.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное название группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMAddGroup.fill_name), IsFSMGroupName())
async def process_name_group_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON()['superadmin']['menu_groups']['add_group_password_text_menu'])
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMAddGroup.fill_password)


# Этот хэндлер будет срабатывать, если во время ввода названия группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddGroup.fill_name))
async def warning_not_name_group(message: Message):
    await message.answer(text=LEXICON()['superadmin']['menu_groups']['false_group_name_FSM'])


# Этот хэндлер будет срабатывать, если введено корректный пароль группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMAddGroup.fill_password), lambda x: 1 <= len(x.text) <= 10)
async def process_password_group_sent(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    # Добавляем в бд группу
    data = await state.get_data()
    await add_group_to_database(name=data['name'], password=data['password'])
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text=LEXICON()['superadmin']['menu_groups']['true_group_FSM'], reply_markup=create_groups_keyboard())


# Этот хэндлер будет срабатывать, если во время ввода пароля группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddGroup.fill_password))
async def warning_not_password_group(message: Message):
    await message.answer(text=LEXICON()['superadmin']['menu_groups']['false_group_password_FSM'])


# ---------------------- меню конкретной группы -------------------------------------------------------------------


# Меню для просмотра пользователей, что состоят в конкретной кгруппе
@router.callback_query(IsGroupCallbackData(), StateFilter(default_state))
async def process_group_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_groups']['group']['text_menu'],
                                         reply_markup=create_group_keyboard(callback.data.split('_')[-1]))
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# ----------------------мену по редактированию админов--------------------------------------------------------------------


# Вызов инлайн клавиатуры со списком админов, при нажатии кнопки админы
@router.callback_query(F.data == 'admins', StateFilter(default_state))
async def process_admins_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['text_menu'],
                                         reply_markup=create_admins_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# Вызов инлайн клавиатуры со списком админов к их удалению, при нажатии кнопки Удалить админа
@router.callback_query(F.data == 'delete_admin', StateFilter(default_state))
async def process_delete_admins_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['delete_admin_text_menu'],
                                         reply_markup=create_delete_admins_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# Удаление админа
@router.callback_query(IsDelAdminCallbackData(), StateFilter(default_state))
async def process_dell_admin_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        del_admin(int(callback.data.split("_")[-1]))
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['delete_admin_text_menu'],
                                         reply_markup=create_delete_admins_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# ----------------------запуск машины состояний по добавлению админа--------------------------------------------------------------------


# Добавление админа
@router.callback_query(F.data == 'add_admin', StateFilter(default_state))
async def process_add_admin_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['add_admin_text_menu'])
    await state.set_state(FSMAssignment.fill_new_admin_id)


# Этот хэндлер будет срабатывать, если введено корректное id
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMAssignment.fill_new_admin_id), IsFSMRightID())
async def process_user_id_sent(message: Message, state: FSMContext):
    # Даем права админа пользователю
    add_admin(message.text)
    await message.answer(text=LEXICON()['superadmin']['menu_admins']['true_id_FSM'])
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода id
# будет введено что-то некорректное
@router.message(StateFilter(FSMAssignment.fill_new_admin_id))
async def warning_not_user_id(message: Message):
    await message.answer(text=LEXICON()['superadmin']['menu_admins']['false_id_FSM'])


# ----------------------общие хендлеры для меню админа и группы--------------------------------------------------------------------


# Реакция на нажатие кнопки Назад, что вернет пользователя в меню суперадмина
@router.callback_query(F.data == 'back_in_superadmin', StateFilter(default_state))
async def process_back_in_superadmin_spress(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['text_menu'],
                             reply_markup=create_superadmin_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()
