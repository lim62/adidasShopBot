from aiogram import Router, F
from aiogram.types import (Message,
                           CallbackQuery,
                           InputMediaPhoto)
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboards import (adminGetStarted,
                       moderGetStarted,
                       userGetStarted,
                       catalogKeyboard)
from utils import failFunction
from database import (db,
                      addToTable,
                      getFromTable)
from lexicon import lexRU, loadProduct

otherRouter = Router()

@otherRouter.message(CommandStart(), StateFilter(default_state))
async def allStart(msg: Message, role: str) -> None:
    if msg.from_user.id not in [row[0] for row in getFromTable('utils')]:
        addToTable('utils', {'id': msg.from_user.id,
                            'username': f'@{msg.from_user.username}',
                            'position': '',
                            'toAdd': '',
                            'toDelete': ''})
    if role == 'admin':
        if f'@{msg.from_user.username}' not in [row[0] for row in getFromTable('moder')]:
            addToTable('moder', {'username': f'@{msg.from_user.username}'})
    match role:
        case 'admin':
            text = lexRU['message']['adminStart']
            markup = adminGetStarted()
        case 'moder':
            text = lexRU['message']['moderStart']
            markup = moderGetStarted()
        case _: 
            text = lexRU['message']['userStart']
            markup = userGetStarted()
    await msg.answer(text=text,
                     reply_markup=markup)

@otherRouter.callback_query(F.data == 'catalog')
async def userCatalog(call: CallbackQuery, role: str) -> None:
    isUser = True if role == 'user' else False
    await call.message.delete()
    await call.message.answer_photo(photo=lexRU['images']['logo'],
                                    caption=lexRU['message']['catalog'],
                                    reply_markup=catalogKeyboard(cats=getFromTable('categories'),
                                                                 prods=getFromTable('products'),
                                                                 isUser=isUser))

@otherRouter.callback_query(F.data.contains('Category'))
async def moderChangeCategory(call: CallbackQuery, role: str) -> None:
    category = str(call.data)[:-8]
    db['position'][call.from_user.id] += f'{category}:'
    position = db['position'][call.from_user.id].split(':')[:-1]
    toDisplay: dict = db['products']
    for cat in position:
        toDisplay = toDisplay[cat]
    isUser = True if role == 'user' else False
    await call.message.edit_caption(caption=f'<b>{category}:</b>',
                                    reply_markup=catalogKeyboard(toDisplay,
                                                                 inCategory=True,
                                                                 isUser=isUser))

@otherRouter.callback_query(F.data.contains('Product'))
async def moderShowProduct(call: CallbackQuery, role: str) -> None:
    name = str(call.data)[:-7]
    position = db['position'][call.from_user.id].split(':')[:-1]
    array: dict = db['products']
    for cat in position:
        array = array[cat]
    toDisplay = array[name]
    db['position'][call.from_user.id] += f'{name}:'
    isUser = True if role == 'user' else False
    await call.message.edit_media(media=InputMediaPhoto(media=toDisplay[-1]))
    await call.message.edit_caption(caption=loadProduct(toDisplay),
                                    reply_markup=catalogKeyboard(toDisplay,
                                                                 inProduct=True,
                                                                 isUser=isUser))

@otherRouter.callback_query(F.data == 'no')
@otherRouter.callback_query(F.data == 'cancel')
async def allNo(call: CallbackQuery, state: FSMContext, role: str) -> None:
    info = failFunction(role)
    db['position'][call.from_user.id] = ''
    await call.message.edit_text(text=info[0],
                                 reply_markup=info[1])
    await state.clear()

@otherRouter.callback_query(F.data == 'cancelPhoto')
async def userCancelPhoto(call: CallbackQuery, state: FSMContext, role: str) -> None:
    info = failFunction(role)
    db['position'][call.from_user.id] = ''
    await call.message.delete()
    await call.message.answer(text=info[0],
                              reply_markup=info[1])
    await state.clear()

@otherRouter.message()
async def allElse(msg: Message) -> None:
    await msg.answer(lexRU['message']['else'])