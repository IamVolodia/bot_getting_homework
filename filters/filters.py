from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from models.functions import get_subject_by_id_and_group_id, get_user, get_group_by_name, get_subject_by_name, get_all_subjects_by_group


# Фильтр который проверяет правильность ввода имени группы и есть ли она в базе данных
class IsFSMGroupName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = True
        if 1 <= len(message.text) <= 100:
            data = get_group_by_name(message.text)
            if data == []:
                data = True
            else:
                data = False
        else:
            data = False
        return data


#-------------------фильтры суперадмина--------------------------------------------------------------


# Фильтр который отлавливает callback по уделению права админа
class IsDelAdminCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('del_admin_id')

# Фильтр который отлавливает callback по удалению группы из бд
class IsDelGroupCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('del_group_id')


# Фильтр который отлавливает callback по просмотру пользователей группы
class IsGroupCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('group_id')


# Фильтр который проверяет правильность ввода id пользователя и есть ли он в базе данных
class IsFSMRightID(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = True
        if message.text.isdigit():
            data = get_user(message.text)
            if data == []:
                data = False
            else:
                data = True
        else:
            data = False
        return data


#-------------------фильтры админа--------------------------------------------------------------


# Фильтр который проверяет при команде start есть ли у пользователя права админа
# от этого будет зависеть, какую инлайн клавиатуру ему отправит бот
class IsUserHaveStatusAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = get_user(message.from_user.id)
        if data == []:
            return False
        return data[0][-2] == 1


# Фильтр который ловит callback на назначение прав админа пользователю
class IsAddStatusAdmin(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_add_status_admin_')


# Фильтр который ловит callback на удаление прав админа пользователя
class IsDelStatusAdmin(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_del_status_admin_')


# Фильтр который ловит callback на удаление пользователя из группы
class IsDelUserFromGroup(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_del_user_')


# Фильтр который ловит callback на удаление  группы
class IsDelGroup(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_del_group_')


# Фильтр который ловит callback на удаление предмета из группы
class IsDelSubjectFromGroup(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_del_subject_')


# Фильтр который проверяет правильность ввода имени предмета и есть ли она в базе данных
class IsFSMSubjectName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if 1 <= len(message.text) <= 100:
            group_id = get_user(message.from_user.id)[-1][-1]
            data = get_subject_by_name(message.text, group_id)
            if not data:
                return True
        return False


# Фильтр который ловит callback на меню конкретного предмета
class IsSubjectFromGroup(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_subject_id_')


# Фильтр который ловит callback на дату
class IsRightDate(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_date_') and all(i.isdigit() for i in callback.data.split('_')[-3:])


# Фильтр который ловит callback на добавление ДЗ
class IsAddHomework(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_add_homework_')


# Фильтр который ловит callback на удаление ДЗ
class IsDelHomework(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_del_homework_')
    

# Фильтр который проверяет, есть ли предметы у группы
class IsGroupHaveSubject(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        # Получаем group_id
        group_id = get_user(callback.from_user.id)[-1][-1]
        # Получаем все предметы группы
        data = get_all_subjects_by_group(group_id)
        return data


# Фильтр который проверят, есть ли такой предмет в базе данных в данной группе
class SubjectExistsInGroup(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        group_id = get_user(callback.from_user.id)[-1][-1]
        data = get_subject_by_id_and_group_id(callback.data.split("_")[-1], group_id)
        return data


# Фильтр который ловит callback на ретный предмет по которому есть дз в конкретной дате
class IsSubjectFromCalendar(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_date_subject_id_')


# Фильтр который ловит callback на удаление домашнего задания у предмета за конкрентую дату
class IsDelHomeworkFromSubjectForDate(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('admin_date_del_homework_subject_id_')


#-------------------фильтры юзера---------------------------------------------------------------


# Фильтр который проверяет при команде start состоит ли пользователь в группе
# от этого будет зависеть, какую инлайн клавиатуру ему отправит бот
class IsUserNotHaveGroup(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = get_user(message.from_user.id)
        return data == [] or data[0][-1] == None


# Фильтр который проверяет существует ли группа с таким именем
class IsGroupByThatName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = get_group_by_name(message.text)
        return data[0]
