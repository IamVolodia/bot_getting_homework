from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from models.functions import get_user


class IsDelUserCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('del_user_id')


class IsDelGroupCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith('del_group_id')

class IsFSMRightID(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit():
            data = get_user(message.text)
        else:
            data = False
        return data == True