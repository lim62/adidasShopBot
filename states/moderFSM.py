from aiogram.fsm.state import State, StatesGroup

class TheModerFSM(StatesGroup):
    categoryName = State()
    productName = State()
    productDescription = State()
    productPrice = State()
    productPhoto = State()
    sureClear = State()
    deleteCategory = State()
    deleteProduct = State()