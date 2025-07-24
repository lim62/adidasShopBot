from aiogram.types import InlineKeyboardMarkup
from keyboards import (adminGetStarted,
                       moderGetStarted)

def getMarkup(role: str) -> InlineKeyboardMarkup:
    match role:
        case 'admin':
            return adminGetStarted()
        case _:
            return moderGetStarted()