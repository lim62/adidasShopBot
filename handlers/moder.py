from aiogram import Router, F
from aiogram.types import (Message,
                           CallbackQuery)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from filters import IsModerFilter
from database import (addToTable,
                      updateFromTable,
                      getFromTable,
                      deleteFromTable,
                      clearTable)
from states import TheModerFSM
from utils import getMarkup
from lexicon import (lexRU,
                     getDatabase,
                     getOrders)
from keyboards import  (cancelKeyboard,
                       clearOrdersKeyboard,
                       yesOrNo)

moderRouter = Router()
moderRouter.message.filter(IsModerFilter())
moderRouter.callback_query.filter(IsModerFilter())

@moderRouter.callback_query(F.data == 'addCategory')
async def moderAskCategory(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(lexRU['message']['categoryName'],
                              reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.categoryName)

@moderRouter.message(StateFilter(TheModerFSM.categoryName))
async def moderAddCategory(msg: Message, state: FSMContext, role: str) -> None:
    position = getFromTable('utils', f'WHERE id = {msg.from_user.id}')[0][2]
    addToTable('categories', {'name': msg.text, 'position': position})
    await msg.answer(lexRU['message']['categoryAdded'],
                     reply_markup=getMarkup(role))
    await state.clear()

@moderRouter.callback_query(F.data == 'addProduct')
async def moderAskProductName(call: CallbackQuery, state: FSMContext) -> None:
    updateFromTable('utils',
                    {'id': call.from_user.id},
                    {'toAdd': ''})
    await call.message.delete()
    await call.message.answer(lexRU['message']['askName'],
                              reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productName)

@moderRouter.message(StateFilter(TheModerFSM.productName))
async def moderAskProductDescription(msg: Message, state: FSMContext) -> None:
    updateFromTable('utils',
                    {'id': msg.from_user.id},
                    {'toAdd': f'{msg.text}:'})
    await msg.answer(lexRU['message']['askDescription'],
                     reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productDescription)

@moderRouter.message(StateFilter(TheModerFSM.productDescription))
async def moderAskProductPrice(msg: Message, state: FSMContext) -> None:
    past = getFromTable('utils', f'WHERE id = {msg.from_user.id}')[0][3]
    updateFromTable('utils',
                    {'id': msg.from_user.id},
                    {'toAdd': f'{past}{msg.text}:'})
    await msg.answer(lexRU['message']['askPrice'],
                     reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productPrice)

@moderRouter.message(StateFilter(TheModerFSM.productPrice))
async def moderAskProductPhoto(msg: Message, state: FSMContext) -> None:
    past = getFromTable('utils', f'WHERE id = {msg.from_user.id}')[0][3]
    updateFromTable('utils',
                    {'id': msg.from_user.id},
                    {'toAdd': f'{past}{msg.text}:'})
    await msg.answer(lexRU['message']['askPhoto'],
                     reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productPhoto)

@moderRouter.message(F.photo, StateFilter(TheModerFSM.productPhoto))
async def moderProductAdded(msg: Message, state: FSMContext, role: str) -> None:
    position = getFromTable('utils', f'WHERE id = {msg.from_user.id}')[0][2]
    toAdd = [element for element in\
             f"{getFromTable('utils', f'WHERE id = {msg.from_user.id}')[0][3]}{msg.photo[0].file_id}".split(':')]
    addToTable('products', {'name': toAdd[0],
                            'description': toAdd[1],
                            'price': toAdd[2],
                            'photo': toAdd[3],
                            'position': position})
    await msg.answer(lexRU['message']['successModer'],
                     reply_markup=getMarkup(role))
    await state.clear()

@moderRouter.message(StateFilter(TheModerFSM.productPhoto))
async def moderIncorrectPhoto(msg: Message) -> None:
    await msg.answer(lexRU['message']['irregularData'],
                     reply_markup=cancelKeyboard())

@moderRouter.callback_query(F.data == 'deleteCat')
async def moderSureTodeleteCategory(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(lexRU['message']['areSure'],
                              reply_markup=yesOrNo())
    await state.set_state(TheModerFSM.deleteCategory)


@moderRouter.callback_query(F.data == 'deleteProd')
async def moderSureTodeleteProduct(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(lexRU['message']['areSure'],
                              reply_markup=yesOrNo())
    await state.set_state(TheModerFSM.deleteProduct)

@moderRouter.callback_query(F.data == 'yes', StateFilter(TheModerFSM.deleteCategory))
@moderRouter.callback_query(F.data == 'yes', StateFilter(TheModerFSM.deleteProduct))
async def moderDelete(call: CallbackQuery, state: FSMContext, role: str) -> None:
    position = getFromTable('utils', f'WHERE id = {call.from_user.id}')[0][2].split(':')[:-1]
    name = position[-1]
    currentState = await state.get_state()
    if currentState == TheModerFSM.deleteCategory:
        deleteFromTable('categories', key='name', value=name)
    elif currentState == TheModerFSM.deleteProduct:
        deleteFromTable('products', key='name', value=name)
    await call.message.edit_text(lexRU['message']['successModer'],
                                 reply_markup=getMarkup(role))
    await state.clear()


@moderRouter.callback_query(F.data == 'database')
async def moderDatabase(call: CallbackQuery) -> None:
    await call.message.edit_text(getDatabase(),
                                 reply_markup=cancelKeyboard())

@moderRouter.callback_query(F.data == 'orders')
async def moderSeeUser(call: CallbackQuery) -> None:
    if not getFromTable('orders'):
        await call.message.edit_text(lexRU['message']['noOrders'],
                                     reply_markup=cancelKeyboard())
    else: 
        await call.message.edit_text(getOrders(),
                                     reply_markup=clearOrdersKeyboard())

@moderRouter.callback_query(F.data == 'clear')
async def moderSureClear(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(lexRU['message']['areSure'],
                                 reply_markup=yesOrNo())
    await state.set_state(TheModerFSM.sureClear)

@moderRouter.callback_query(F.data == 'yes', StateFilter(TheModerFSM.sureClear))
async def moderClear(call: CallbackQuery, state: FSMContext, role: str) -> None:
    clearTable('orders')
    await call.message.edit_text(lexRU['message']['successModer'],
                                 reply_markup=getMarkup(role))
    await state.clear() 