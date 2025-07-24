from aiogram.fsm.state import State, StatesGroup

class TheAdminFSM(StatesGroup):
    username = State()
    deleteModer = State()