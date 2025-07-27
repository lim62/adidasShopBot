from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from lexicon import lexRU
from states import TheUserFSM
from database import (addToTable,
                      getFromTable)
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
    position = getFromTable('utils', f'WHERE id = {call.from_user.id}')[0][2].split(':')[:-1]
    name = position[-1]
    addToTable('orders',
               {'username': f'@{call.from_user.username}', 
                'product': name})
    await state.clear()
    await call.message.edit_text(lexRU['message']['successUser'],
                                 reply_markup=userGetStarted())