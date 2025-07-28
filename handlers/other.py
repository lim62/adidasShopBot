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
from database import (addToTable,
                      updateFromTable,
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
    updateFromTable('utils',
                    {'id': call.from_user.id},
                    {'position': '', 'toAdd': ''})
    await call.message.delete()
    await call.message.answer_photo(photo=lexRU['images']['logo'],
                                    caption=lexRU['message']['catalog'],
                                    reply_markup=catalogKeyboard(cats=getFromTable('categories', 'WHERE position = \'\''),
                                                                 prods=getFromTable('products', 'WHERE position = \'\''),
                                                                 isUser=isUser))

@otherRouter.callback_query(F.data.contains('Category'))
async def changeCategory(call: CallbackQuery, role: str) -> None:
    category = str(call.data)[:-8]
    position = getFromTable('utils', f'WHERE id = {call.from_user.id}')[0][2]
    updateFromTable(
        'utils',
        {'id': call.from_user.id},
        {'position': f"{position}{category}:"}
    )
    position = getFromTable('utils', f'WHERE id = {call.from_user.id}')[0][2]
    isUser = True if role == 'user' else False
    await call.message.edit_caption(caption=f'<b>{category}: 👇</b>',
                                    reply_markup=catalogKeyboard(cats=getFromTable('categories', f"WHERE position = '{position}'"),
                                                                 prods=getFromTable('products', f"WHERE position = '{position}'"),
                                                                 inCategory=True,
                                                                 isUser=isUser))

@otherRouter.callback_query(F.data.contains('Product'))
async def showProduct(call: CallbackQuery, role: str) -> None:
    name = str(call.data)[:-7]
    position = getFromTable('utils', f'WHERE id = {call.from_user.id}')[0][2]
    updateFromTable(
        'utils',
        {'id': call.from_user.id},
        {'position': f"{position}{name}:"}
    )
    products = getFromTable('products', f"WHERE position = '{position}'")
    trueProduct: tuple
    for product in products:
        if product[0] == name:
            trueProduct = product
            break
    isUser = True if role == 'user' else False
    await call.message.edit_media(media=InputMediaPhoto(media=trueProduct[3]))
    await call.message.edit_caption(caption=loadProduct(trueProduct),
                                    reply_markup=catalogKeyboard(inProduct=True,
                                                                 isUser=isUser))

@otherRouter.callback_query(F.data == 'no')
@otherRouter.callback_query(F.data == 'cancel')
async def allNo(call: CallbackQuery, state: FSMContext, role: str) -> None:
    info = failFunction(role)
    await call.message.edit_text(text=info[0],
                                 reply_markup=info[1])
    await state.clear()

@otherRouter.callback_query(F.data == 'cancelPhoto')
async def userCancelPhoto(call: CallbackQuery, state: FSMContext, role: str) -> None:
    info = failFunction(role)
    await call.message.delete()
    await call.message.answer(text=info[0],
                              reply_markup=info[1])
    await state.clear()

@otherRouter.message()
async def allElse(msg: Message) -> None:
    await msg.answer(lexRU['message']['else'])