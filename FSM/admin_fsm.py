from aiogram.fsm.state import State, StatesGroup

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по добавлению предмета
class FSMCreatSubject(StatesGroup):
    fill_name = State()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний по добавлению домашнего задания
class FSMAddHomework(StatesGroup):
    fill_date = State()
    fill_subject_name = State()
    fill_message = State()