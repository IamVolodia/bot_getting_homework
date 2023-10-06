from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.superadmin_kb import *
from config_data.config import load_config
from lexicon.lexicon import LEXICON
from models.functions import del_admin, add_admin
from filters.filters import IsDelUserCallbackData, IsFSMRightID
from aiogram.fsm.state import default_state
from FSM.superadmin_fsm import FSMAssignment

router = Router()


# Вызов инлайн клавиатуры суперадмина
@router.message(Command(commands='superadmin'), StateFilter(default_state))
async def process_superadmin_command(message: Message):
    if message.from_user.id in load_config().tg_bot.superadmin_ids:
        await message.answer(text=LEXICON()['superadmin']['text_menu'],
                             reply_markup=create_superadmin_keyboard())
    else:
        await message.answer(text=LEXICON()['superadmin']['no_rights'])



# Вызов инлайн клавиатуры со списком групп, при нажатии кнопки группы
@router.callback_query(F.data == 'groups', StateFilter(default_state))
async def process_groups_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_groups']['text_menu'],
                                         reply_markup=create_groups_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()

# Вызов инлайн клавиатуры со списком админов, при нажатии кнопки админы
@router.callback_query(F.data == 'admins', StateFilter(default_state))
async def process_admins_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['text_menu'],
                                         reply_markup=create_admins_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# Вызов инлайн клавиатуры со списком админов к их удалению, при нажатии кнопки удалить админа
@router.callback_query(F.data == 'delete_admin', StateFilter(default_state))
async def process_delete_admins_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['delete_admin_text_menu'],
                                         reply_markup=create_delete_admins_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


# Удаление админа
@router.callback_query(IsDelUserCallbackData(), StateFilter(default_state))
async def process_dell_admin_press(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        del_admin(int(callback.data.split("_")[-1]))
        await callback.message.edit_text(text=LEXICON()['superadmin']['menu_admins']['delete_admin_text_menu'],
                                         reply_markup=create_delete_admins_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()


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



# Вызов инлайн клавиатуры со списком админов, при нажатии кнопки админы
@router.callback_query(F.data == 'back_in_superadmin', StateFilter(default_state))
async def process_back_in_superadmin_spress(callback: CallbackQuery):
    if callback.from_user.id in load_config().tg_bot.superadmin_ids:
        await callback.message.edit_text(text=LEXICON()['superadmin']['text_menu'],
                             reply_markup=create_superadmin_keyboard())
    else:
        await callback.answer(text=LEXICON()['superadmin']['no_rights'])

    await callback.answer()
