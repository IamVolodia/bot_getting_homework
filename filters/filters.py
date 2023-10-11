from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from models.functions import get_user, get_group_by_name


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


#-------------------фильтры админа--------------------------------------------------------------


# Фильтр который проверяет при команде start есть ли у пользователя права админа
# от этого будет зависеть, какую инлайн клавиатуру ему отправит бот
class IsUserHaveStatusAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = get_user(message.from_user.id)
        return data == [] or data[0][-2] == 1


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


#-------------------фильтры юзера---------------------------------------------------------------


# Фильтр который проверяет при команде start состоит ли пользователь в группе
# от этого будет зависеть, какую инлайн клавиатуру ему отправит бот
class IsUserNotHaveGroup(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        data = get_user(message.from_user.id)
        return data == [] or data[0][-1] == None