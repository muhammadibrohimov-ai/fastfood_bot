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
        [KeyboardButton(text="Menu"), KeyboardButton(text="Buyurtmalarim")],
        [KeyboardButton(text="Aloqa"), KeyboardButton(text = "Sozlamalar")],
        [KeyboardButton(text = "Admin panelga o'tish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
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
        [KeyboardButton(text="Menu"), KeyboardButton(text="Buyurtmalarim")],
        [KeyboardButton(text="Aloqa"), KeyboardButton(text = "Sozlamalar")],
        [KeyboardButton(text = "Admin panelga o'tish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

async def inline_keyboard_menu():
    keyboard = InlineKeyboardBuilder()
    
    if get_foods():
        for i in get_foods():
            keyboard.add(InlineKeyboardButton(text = i[1], callback_data=f'food_{i[0]}'))
            
    else:
        keyboard.add(InlineKeyboardButton(text = "Hozircha ovqat mavjud emas, ortga qayting", callback_data='main'))
        
    return keyboard.adjust(2).as_markup()
    
    
    
async def one_food_inline_button(food_id ,i:int = 1) :
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text = '-', callback_data=f'minus_{i}_{food_id}'), 
                InlineKeyboardButton(text = f'{i}', callback_data = 'nothing'), 
                InlineKeyboardButton(text = '+', callback_data=f'plus_{i}_{food_id}')
            ],
            [
                InlineKeyboardButton(text = "Ortga qaytish", callback_data = f"back_{food_id}"),
                InlineKeyboardButton(text = 'Savatga qo\'shish', callback_data = f"order_{i}_{food_id}")
            ]
        ]
        )   
    return keyboard


async def send_cancel_food(quantity, food_id):
    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text = "CANCEL", callback_data=f"back_{quantity}_{food_id}"), 
                            InlineKeyboardButton(text = 'SEND', callback_data=f"send_{quantity}_{food_id}")
                        ]
                    ]
                )
    
    return keyboard



admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Taomlar"), KeyboardButton(text = "Buyurtmalar")],
        [KeyboardButton(text = "Xabarlar"),KeyboardButton(text = "Foydalanuvchilar")],
        [KeyboardButton(text = "User panelga qaytish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

add_foods = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Yangi taom qo'shish", callback_data="new_food")],
        [InlineKeyboardButton(text = 'Mavjud taomni o\'zgartirish', callback_data="existing_food")],
        [InlineKeyboardButton(text = "Taomlar ro'yxati", callback_data ='show_foods')]
    ]
)

back_button = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text = 'Back')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def inline_keyboard_foods(food_id):
    features = ['name', 'price', 'image', 'quantity', 'description',"❌Delete"]
    keyboard = InlineKeyboardBuilder()
    
    for i in features:
        keyboard.add(InlineKeyboardButton(text = i, callback_data=f'edit_{food_id}_{features.index(i)}'))
    
        
    return keyboard.adjust(2).as_markup()

order_show = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "🆕New"),
            KeyboardButton(text = "In progress"),
        ],
        [
            KeyboardButton(text = "Finished"),
            KeyboardButton(text = 'Canceled')    
        ],
        [
            KeyboardButton(text = "Back")  
        ]
    ], 
    resize_keyboard=True,
    one_time_keyboard=True
)

async def order_inline_kb(order_id:int, i:int = 1):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text = '❌Cancel', callback_data=f'cancel_{order_id}'),
                InlineKeyboardButton(text = f"{'In progress' if i==1 else  'Finish'}", callback_data=f"{'progress' if i==1 else 'finish'}_{order_id}")
            ]
        ]
    )
    
    
settings = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Ismni o'zgartirish")],
                [KeyboardButton(text="Telefon raqamni o'zgartirish")],
                [KeyboardButton(text="Joylashuvni o'zgartirish")],
                [KeyboardButton(text="🔙 Ortga")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )