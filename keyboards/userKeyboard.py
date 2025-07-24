from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import lexRU

def userGetStarted() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexRU['button']['catalog'],
                                                                       callback_data='catalog')]])