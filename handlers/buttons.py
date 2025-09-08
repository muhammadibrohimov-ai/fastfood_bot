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

from database import get_foods

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

async def inline_keyboard_menu():
    keyboard = InlineKeyboardBuilder()
    
    for i in get_foods():
        keyboard.add(InlineKeyboardButton(text = i[1], callback_data=f'food_{i[0]}'))
        
    return keyboard.adjust(2).as_markup()
    
    
async def one_food_inline_button(i:int = 0) :
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text = '-', callback_data=f'method_1'), 
                InlineKeyboardButton(text = f'{0+i}', callback_data = 'method_3'), 
                InlineKeyboardButton(text = '+', callback_data=f'method_2')
            ],
            [InlineKeyboardButton(text = 'Savatga qo\'shish', callback_data = "order")]
        ]
        )   
    return keyboard