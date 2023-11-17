from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.admin_kb import *
from keyboards.calendar_kb import *
from lexicon.lexicon import LEXICON
from models.methods import add_user_to_database, add_subject_to_database
from models.functions import (del_admin, add_admin, del_group,
                              del_user_from_group, del_subject, get_subject_by_id,
                              del_homework_from_sebject_for_date, change_name_group, change_password_group)
from filters.filters import (IsUserHaveStatusAdmin, IsAddStatusAdmin, IsDelStatusAdmin,
                             IsDelUserFromGroup, IsDelGroup, IsDelSubjectFromGroup,
                             IsFSMSubjectName, IsDelHomeworkFromSubjectForDate, IsRightDate,
                             IsGroupHaveSubject, IsAddHomework, SubjectExistsInGroup,
                             IsSubjectFromCalendar, IsDelHomework, IsFSMGroupName, IsCorrectMessageToAdd)
from aiogram.fsm.state import default_state
from FSM.admin_fsm import *
from utils.message_converter import save_message_to_database, get_homeworks_from_database


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
                         reply_markup=create_calendar_keyboard(status="admin", date=callback.message.date, callback=callback))


# Меню админа - календарь - другой месяц
@router.callback_query(F.data.startswith('admin_calendar_another_month_'), StateFilter(default_state))
async def process_admin_calendar_another_month_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['text_menu'],
                         reply_markup=create_calendar_keyboard(status="admin", date=callback.data, callback=callback))


# Меню админа - календарь - конкретная дата
@router.callback_query(IsRightDate(), StateFilter(default_state))
async def process_admin_calendar_date_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['text_menu'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=callback.from_user.id, date=callback.data))


#----------------------открытие календаря в главном меню - запуск машины состояний по добавлению дз-----------------------------


# Хендлер на запуск машины состояний по добавлению дз
@router.callback_query(IsAddHomework(), StateFilter(default_state), IsGroupHaveSubject())
async def process_admin_add_homework_press(callback: CallbackQuery, state: FSMContext):
    date = '-'.join(callback.data.split("_")[-3:])
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['choice_subject'],
                                     reply_markup=create_FSM_all_subjects_keyboard(callback.from_user.id, date))
    await state.update_data(date=date)
    await state.set_state(FSMAddHomework.fill_subject_name)


# Если у группы нет предметов, то будет отправлено соответсвующее собщение и машина состояний не будет запущена
@router.callback_query(IsAddHomework(), StateFilter(default_state))
async def process_admin_add_homework_wrong_press(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['group_havent_subjects'],
                                     show_alert=True)


# Этот хэндлер будет срабатывать на кнопку назад в списке предметов
@router.callback_query(StateFilter(FSMAddHomework.fill_subject_name), F.data.startswith("admin_back_to_menu_date_from_FSM"))
async def process_admin_back_to_menu_date_from_FSM_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['text_menu'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=callback.from_user.id, date=callback.data))
    await state.clear()


# Этот хэндлер будет срабатывать на название предмета
@router.callback_query(StateFilter(FSMAddHomework.fill_subject_name), SubjectExistsInGroup())
async def process_admin_name_subject_for_homework_sent(callback: CallbackQuery, state: FSMContext):
    subject_id = callback.data.split('_')[-1]
    await state.update_data(subject_id=subject_id)
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['sent_homework'])
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMAddHomework.fill_message)


# Этот хэндлер будет срабатывать, если название предмета было введено, а не выбрано из списка
@router.message(StateFilter(FSMAddHomework.fill_subject_name))
async def warning_admin_name_subject_for_homework_sent(message: CallbackQuery, state: FSMContext):
    await message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['warning_subject'],
                                     reply_markup=create_FSM_all_subjects_keyboard(message.from_user.id))


# Этот хэндлер будет срабатывать на отправленое сообщнение и добавлять его в базу данных
@router.message(StateFilter(FSMAddHomework.fill_message), IsCorrectMessageToAdd())
async def process_admin_message_save_to_db(message: Message, state: FSMContext):
    # Получаем данные из машины состояний
    data = await state.get_data()
    # Добавляем домашнее задание в базу данных
    await save_message_to_database(date=data["date"], subject_id=data["subject_id"], message=message)
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['successful_add'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=message.from_user.id, date=data["date"].replace('-', '_')))


# Этот хэндлер будет срабатывать на отправленое сообщнение, которое не подходит по типу
@router.message(StateFilter(FSMAddHomework.fill_message))
async def warning_admin_message_save_to_db(message: Message, state: FSMContext):
    await message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['FSM_add_homework']['warning_homework'])

#----------------------открытие календаря в главном меню - выбор даты -------------------------------------------


# Хендлер на конкретный предмет за определенную дату
@router.callback_query(IsSubjectFromCalendar(), StateFilter(default_state))
async def process_admin_subject_in_date_press(callback: CallbackQuery):
    # Получаем id предмета и даду
    subject_id, date = callback.data.split("_")[-2:]
    # Плучаем название предмета по id
    subject_name = get_subject_by_id(subject_id)
    # Отправляем сообщением название предмета, по которому необходимо дз
    await callback.message.answer(text=f"Домашние задания по {subject_name[0][1]} за {date}:")
    # Отправка сообщение всей домашней работы по выбраному предмету за эту дату
    await get_homeworks_from_database(date=date, subject_id=subject_id, callback=callback)
    await callback.message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['text_menu'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=callback.from_user.id, date=date.replace('-', '_')))


# Получение всех домашних заданий за определенную дату
@router.callback_query(F.data.startswith('admin_get_all_homework'), StateFilter(default_state))
async def process_admin_subject_in_date_press(callback: CallbackQuery):
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
    await callback.message.answer(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['text_menu'],
                         reply_markup=create_admin_menu_date_keyboard(user_id=callback.from_user.id, date=date.replace('-', '_')))



#---------------------инлайн клавиатура с предмета по которым необходимо удалить домашнее задание--------------------


# Меню конкретной даты со списком предметов к удалению у них дз
@router.callback_query(IsDelHomework(), StateFilter(default_state))
async def process_admin_del_homework_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['admin_del_homework']['text_menu'],
                                     reply_markup=create_admin_menu_del_homework_keyboard(callback.from_user.id, date=callback.data))


# Удаление домашнего задания у конкреного предмета
@router.callback_query(IsDelHomeworkFromSubjectForDate(), StateFilter(default_state))
async def process_del_homework_from_sebject_for_date_press(callback: CallbackQuery):
    subject_id, date = callback.data.split("_")[-2:]
    # Удаление домашнего задания у предмета за дату
    del_homework_from_sebject_for_date(subject_id, date)
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_calendar']['admin_menu_date']['admin_del_homework']['text_menu'],
                                     reply_markup=create_admin_menu_del_homework_keyboard(callback.from_user.id, date=callback.data.split("_")[-1].replace('-', '_')))


#---------------------------------полученеи домашнего задания на завтра-------------------------------------------------------------


# Хендлер на получение домашнего задания на завтра
@router.callback_query(F.data.startswith('admin_today'), StateFilter(default_state))
async def process_admin_homework_today_press(callback: CallbackQuery):
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
        await callback.message.answer(text=LEXICON()['admin']['text_menu'],
                            reply_markup=create_start_keyboard_if_admin())
    else:
        await callback.answer(text=LEXICON()['admin']['no_homework_today'],
                              show_alert=True)



#---------------------------------меню группы----------------------------------------------------------------------


# Хендлер на получение домашнего задания на завтра
@router.callback_query(F.data.startswith('admin_menu_group'), StateFilter(default_state))
async def process_admin_menu_group_press(callback: CallbackQuery):
    # Изменяем инлайн клавиатуру
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_group']['text_menu'],
                                  reply_markup=create_admin_menu_group_keyboard(callback.from_user.id))
    

#---------------------------------запуск машины состояний по изменению имени----------------------------------------   


# Хендлер на получение домашнего задания на завтра
@router.callback_query(F.data.startswith('admin_change_name_group'), StateFilter(default_state))
async def process_admin_change_name_group_press(callback: CallbackQuery, state: FSMContext):
    # Изменяем инлайн клавиатуру
    await callback.message.answer(text=LEXICON()['admin']['admin_menu_group']['FSM_change_name_group']["sent_name"])
    await state.set_state(FSMChangeNameGroup.fill_name)

# Этот хэндлер будет срабатывать, если введено корректное название группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMChangeNameGroup.fill_name), IsFSMGroupName())
async def process_admin_name_group_sent(message: Message, state: FSMContext):
    # Получаем id группы
    group_id = get_user(message.from_user.id)[-1][-1]
    # Изменяем имя группы
    change_name_group(group_id, message.text)
    await message.answer(text=LEXICON()['admin']['admin_menu_group']['FSM_change_name_group']["successful_change"],
                                  reply_markup=create_admin_menu_group_keyboard(message.from_user.id))
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода названия группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMChangeNameGroup.fill_name))
async def warning_admin_not_name_group(message: Message):
    await message.answer(text=LEXICON()['admin']['admin_menu_group']['FSM_change_name_group']["warning_name"])


#---------------------------------запуск машины состояний по изменению пароля----------------------------------------   


# Хендлер на получение домашнего задания на завтра
@router.callback_query(F.data.startswith('admin_change_password_group'), StateFilter(default_state))
async def process_admin_change_password_group_press(callback: CallbackQuery, state: FSMContext):
    # Изменяем инлайн клавиатуру
    await callback.message.answer(text=LEXICON()['admin']['admin_menu_group']['FSM_change_password_group']["sent_password"])
    await state.set_state(FSMChangePasswordGroup.fill_password)

# Этот хэндлер будет срабатывать, если введено корректное название группы
# и переводить в состояние ожидания ввода пароля
@router.message(StateFilter(FSMChangePasswordGroup.fill_password), lambda x: 1 <= len(x.text) <= 10)
async def process_admin_password_group_sent(message: Message, state: FSMContext):
    # Получаем id группы
    group_id = get_user(message.from_user.id)[-1][-1]
    # Изменяем имя группы
    change_password_group(group_id, message.text)
    await message.answer(text=LEXICON()['admin']['admin_menu_group']['FSM_change_password_group']["successful_change"],
                                  reply_markup=create_admin_menu_group_keyboard(message.from_user.id))
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода названия группы
# будет введено что-то некорректное
@router.message(StateFilter(FSMChangeNameGroup.fill_name))
async def warning_admin_not_name_group(message: Message):
    await message.answer(text=LEXICON()['admin']['admin_menu_group']['FSM_change_password_group']["warning_password"])


#---------------------хендлеры по нажатию кнопки 'назад'--------------------------------------------------------


# Кнопка возвращение в меню конкрентной даты
@router.callback_query(F.data == 'admin_back_to_menu', StateFilter(default_state))
async def process_admin_users_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())

# Кнопка возвращение в меню админа
@router.callback_query(F.data == 'admin_back_to_menu', StateFilter(default_state))
async def process_admin_back_to_menu_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON()['admin']['text_menu'],
                         reply_markup=create_start_keyboard_if_admin())


# Кнопка возвращения в меню со списком пользователей группы
@router.callback_query(F.data == 'admin_back_to_menu_users', StateFilter(default_state))
async def process_admin_back_to_menu_users_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_users']['text_menu'],
                         reply_markup=create_admin_menu_users_keyboard(callback.from_user.id))


# Кнопка возвращения в меню со списком предметов группы
@router.callback_query(F.data == 'admin_back_to_menu_subject')
async def process_admin_back_to_menu_subject_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON()['admin']['admin_menu_subjects']['text_menu'],
                         reply_markup=create_admin_menu_subjects_keyboard(callback.from_user.id))