from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon import lexRU
from filters import IsAdminFilter
from states import TheAdminFSM
from database import (addToTable,
                      updateFromTable,
                      deleteFromTable,
                      getFromTable)
from keyboards import (adminGetStarted,
                       cancelKeyboard,
                       yesOrNo,
                       adminModerator)

adminRouter = Router()
adminRouter.message.filter(IsAdminFilter())
adminRouter.callback_query.filter(IsAdminFilter())

@adminRouter.callback_query(F.data == 'moderator', StateFilter(default_state))
async def adminAddModeratorUsername(call: CallbackQuery) -> None:
    await call.message.edit_text(lexRU['message']['moderator'],
                                 reply_markup=adminModerator())

@adminRouter.callback_query(F.data == 'addModerator', StateFilter(default_state))
async def adminAddModer(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(lexRU['message']['addModerator'],
                                 reply_markup=cancelKeyboard())
    await state.set_state(TheAdminFSM.username)

@adminRouter.message(F.text.startswith('@'), StateFilter(TheAdminFSM.username))
async def adminUsername(msg: Message, state: FSMContext) -> None:
    addToTable('moder', {'username': msg.text})
    await msg.answer(lexRU['message']['successModer'],
                     reply_markup=adminGetStarted())
    await state.clear()

@adminRouter.callback_query(F.data.contains('@'), StateFilter(default_state))
async def adminSureToDeleteModer(call: CallbackQuery, state: FSMContext) -> None:
    updateFromTable('utils', {'id': call.from_user.id, 'toDelete': call.data})
    await call.message.edit_text(lexRU['message']['areSure'],
                                 reply_markup=yesOrNo())
    await state.set_state(TheAdminFSM.deleteModer)

@adminRouter.message(StateFilter(TheAdminFSM.username))
async def adminIrregularUsername(msg: Message) -> None:
    await msg.answer(lexRU['message']['irregularData'],
                     reply_markup=cancelKeyboard())

@adminRouter.callback_query(F.data == 'yes', StateFilter(TheAdminFSM.deleteModer))
async def adminDeleteModer(call: CallbackQuery, state: FSMContext) -> None:
    deleteFromTable('moder',
                    'username',
                    getFromTable('utils', f'WHERE id = {call.from_user.id}')[0][4])
    await call.message.edit_text(lexRU['message']['successModer'],
                                 reply_markup=adminGetStarted())
    await state.clear()
