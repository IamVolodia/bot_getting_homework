from aiogram.fsm.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний
class FSMAssignment(StatesGroup):
    fill_new_admin_id = State()        # Состояние ожидания ввода id юзера, которому будет присвоен статус админа
