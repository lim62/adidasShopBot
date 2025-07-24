from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import lexRU

def moderGetStarted() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexRU['button']['catalog'], callback_data='catalog')],
                                                 [InlineKeyboardButton(text=lexRU['button']['orders'], callback_data='orders')],
                                                 [InlineKeyboardButton(text=lexRU['button']['database'], callback_data='database')]])

def clearOrdersKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexRU['button']['clear'], callback_data='clear')],
                                                 [InlineKeyboardButton(text=lexRU['button']['cancel'], callback_data='cancel')]])
