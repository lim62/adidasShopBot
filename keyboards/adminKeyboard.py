from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import lexRU
from database import getFromTable

def adminGetStarted() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lexRU['button']['moderator'], callback_data='moderator')],
        [InlineKeyboardButton(text=lexRU['button']['catalog'], callback_data='catalog')],
        [InlineKeyboardButton(text=lexRU['button']['orders'], callback_data='orders')],
        [InlineKeyboardButton(text=lexRU['button']['database'], callback_data='database')]
        ])

def adminModerator() -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder()\
        .row(*(InlineKeyboardButton(text=moderator[0], callback_data=str(moderator[0])) for moderator in getFromTable('moder')[1:]), width=1)\
        .row(InlineKeyboardButton(text=lexRU['button']['add'], callback_data='addModerator'), width=1)\
        .row(InlineKeyboardButton(text=lexRU['button']['cancel'], callback_data='cancel'), width=1).as_markup()