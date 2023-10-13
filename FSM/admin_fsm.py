from aiogram.fsm.state import State, StatesGroup

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по добавлению предмета
class FSMCreatSubject(StatesGroup):
    fill_name = State()
