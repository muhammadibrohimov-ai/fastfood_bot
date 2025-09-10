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
    
    
    
async def one_food_inline_button(i:int = 1) :
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text = '-', callback_data=f'minus_{i}'), 
                InlineKeyboardButton(text = f'{i}', callback_data = 'nothing'), 
                InlineKeyboardButton(text = '+', callback_data=f'plus_{i}')
            ],
            [
                InlineKeyboardButton(text = "Ortga qaytish", callback_data = "back"),
                InlineKeyboardButton(text = 'Savatga qo\'shish', callback_data = "order")
            ]
        ]
        )   
    return keyboard



admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Taom qo'shish")],
        [KeyboardButton(text = "Xabarlar")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

add_foods = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = "Yangi taom qo'shish", callback_data="new_food"), 
            InlineKeyboardButton(text = 'Mavjud taomni qo\'shish', callback_data="existing_food")
        ]
    ]
)

async def inline_keyboard_foods():
    keyboard = InlineKeyboardBuilder()
    
    for i in get_foods():
        keyboard.add(InlineKeyboardButton(text = i[1], callback_data=f'existing-food_{i[0]}'))
        
    return keyboard.adjust(2).as_markup()