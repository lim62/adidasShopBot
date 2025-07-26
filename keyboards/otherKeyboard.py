from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import lexRU

def yesOrNo() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lexRU['button']['yes'], callback_data='yes'),
        InlineKeyboardButton(text=lexRU['button']['no'], callback_data='no')]
        ])

def cancelKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lexRU['button']['cancel'], callback_data='cancel')]
        ])

def catalogKeyboard(
        cats: list,
        prods: list,
        inCategory: bool = False,
        inProduct: bool = False,
        isUser: bool = False
    ) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if not inProduct:
        keyboard.row(*(InlineKeyboardButton(text=name, callback_data=f'{name}Category') for name in [row[0] for row in cats]), width=1)\
        .row(*(InlineKeyboardButton(text=name, callback_data=f'{name}Product') for name in [row[0] for row in prods]), width=1)
        if not isUser:
            keyboard.row(InlineKeyboardButton(text=lexRU['button']['addCategory'], callback_data='addCategory'), width=1)\
            .row(InlineKeyboardButton(text=lexRU['button']['addProduct'], callback_data='addProduct'), width=1)
    if inCategory and not isUser:
        keyboard.row(InlineKeyboardButton(text=lexRU['button']['delete'], callback_data='deleteCat'))
    elif inProduct and not isUser:
        keyboard.row(InlineKeyboardButton(text=lexRU['button']['delete'], callback_data='deleteProd'))
    elif inProduct and isUser:
        keyboard.row(InlineKeyboardButton(text=lexRU['button']['buy'], callback_data='buy'))
    keyboard.row(InlineKeyboardButton(text=lexRU['button']['cancel'], callback_data='cancelPhoto'), width=1)
    return keyboard.as_markup()