from aiogram.fsm.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по добавленю прав админа
class FSMAssignment(StatesGroup):
    fill_new_admin_id = State()        # Состояние ожидания ввода id юзера, которому будет присвоен статус админа


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по добавлению группы
class FSMAddGroup(StatesGroup):
    fill_name = State()
    fill_password = State()