from aiogram.fsm.state import State, StatesGroup

class TheUserFSM(StatesGroup):
    sureToBuy = State()