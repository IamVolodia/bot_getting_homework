from aiogram.fsm.state import State, StatesGroup

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по добавлению группы
class FSMCreatGroup(StatesGroup):
    fill_name = State()
    fill_password = State()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по присоеденению к группе
class FSMJoinGroup(StatesGroup):
    fill_name = State()
    fill_password = State()