from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from lexicon import lexRU
from states import TheUserFSM
from database import db
from keyboards import (userGetStarted,
                       yesOrNo)

userRouter = Router()

@userRouter.callback_query(F.data == 'buy')
async def userSureToBuy(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await call.message.answer(lexRU['message']['areSure'],
                              reply_markup=yesOrNo())
    await state.set_state(TheUserFSM.sureToBuy)

@userRouter.callback_query(F.data == 'yes', StateFilter(TheUserFSM.sureToBuy))
async def userBuy(call: CallbackQuery, state: FSMContext) -> None:
    position = db['position'][call.from_user.id].split(':')[:-1]
    array: dict = db['products']
    for cat in position:
        array = array[cat]
    db['orders'][f'@{call.from_user.username}'].append(array[0])
    db['position'][call.from_user.id] = ''
    await state.clear()
    await call.message.edit_text(lexRU['message']['successUser'],
                                 reply_markup=userGetStarted())