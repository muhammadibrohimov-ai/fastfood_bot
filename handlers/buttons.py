from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder
)

register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Register')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

registered_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Menu")],
        [KeyboardButton(text = "Buyurtma")],
        [KeyboardButton(text = "Aloqa")],
        [KeyboardButton(text = "Sozlamalar")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
