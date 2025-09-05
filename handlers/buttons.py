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

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Telefonni jo'natish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Location jo'natish", request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

action_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Asosiy menuga o'tish", callback_data="action")]
    ]
)

action_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Menu")],
        [KeyboardButton(text="Buyurtmalar")],
        [KeyboardButton(text="Aloqa")],
        [KeyboardButton(text='Sozlamalar')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)