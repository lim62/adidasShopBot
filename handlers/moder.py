from aiogram import Router, F
from aiogram.types import (Message,
                           CallbackQuery)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from filters import IsModerFilter
from database import db
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
    position = db['position'][msg.from_user.id].split(':')[:-1]
    toAdd: dict = db['products']
    for cat in position:
        toAdd = toAdd[cat]
    toAdd[msg.text] = {}
    db['position'][msg.from_user.id] = ''
    await msg.answer(lexRU['message']['categoryAdded'],
                     reply_markup=getMarkup(role))
    await state.clear()

@moderRouter.callback_query(F.data == 'addProduct')
async def moderAskProductName(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(lexRU['message']['askName'],
                              reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productName)

@moderRouter.message(StateFilter(TheModerFSM.productName))
async def moderAskProductDescription(msg: Message, state: FSMContext) -> None:
    db['toAdd'][msg.from_user.id].append(msg.text)
    await msg.answer(lexRU['message']['askDescription'],
                     reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productDescription)

@moderRouter.message(StateFilter(TheModerFSM.productDescription))
async def moderAskProductPrice(msg: Message, state: FSMContext) -> None:
    db['toAdd'][msg.from_user.id].append(msg.text)
    await msg.answer(lexRU['message']['askPrice'],
                     reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productPrice)

@moderRouter.message(StateFilter(TheModerFSM.productPrice))
async def moderAskProductPhoto(msg: Message, state: FSMContext) -> None:
    db['toAdd'][msg.from_user.id].append(msg.text)
    await msg.answer(lexRU['message']['askPhoto'],
                     reply_markup=cancelKeyboard())
    await state.set_state(TheModerFSM.productPhoto)

@moderRouter.message(F.photo, StateFilter(TheModerFSM.productPhoto))
async def moderProductAdded(msg: Message, state: FSMContext, role: str) -> None:
    db['toAdd'][msg.from_user.id].append(msg.photo[0].file_id)
    position = db['position'][msg.from_user.id].split(':')[:-1]
    toAdd: dict = db['products']
    for cat in position:
        toAdd = toAdd[cat]
    toAdd[db['toAdd'][msg.from_user.id][0]] = db['toAdd'][msg.from_user.id]
    db['toAdd'][msg.from_user.id] = []
    db['position'][msg.from_user.id] = ''
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
async def moderDeleteCategory(call: CallbackQuery, state: FSMContext, role: str) -> None:
    position = db['position'][call.from_user.id].split(':')[:-1]
    itemRemove = position[-1]
    position = position[:-1]
    toRemove: dict = db['products']
    for cat in position:
        toRemove = toRemove[cat]
    toRemove.pop(itemRemove)
    db['position'][call.from_user.id] = ''
    await call.message.edit_text(lexRU['message']['successModer'],
                                 reply_markup=getMarkup(role))
    await state.clear()

@moderRouter.callback_query(F.data == 'database')
async def moderDatabase(call: CallbackQuery) -> None:
    await call.message.edit_text(getDatabase(),
                                 reply_markup=cancelKeyboard())

@moderRouter.callback_query(F.data == 'orders')
async def moderSeeUser(call: CallbackQuery) -> None:
    if not db['orders']:
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
    db['orders'] = {}
    await call.message.edit_text(lexRU['message']['successModer'],
                                 reply_markup=getMarkup(role))
    await state.clear() 