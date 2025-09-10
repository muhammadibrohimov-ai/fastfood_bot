from aiogram import Router, F
from aiogram.types import (
    Message, 
    CallbackQuery, 
    FSInputFile, 
    InputMediaPhoto
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .buttons import action_kb, inline_keyboard_menu, one_food_inline_button
from database import get_specific_food


action_router = Router()

@action_router.callback_query(F.data.in_(['action',]))
async def start_action(callback:CallbackQuery):
    await callback.message.answer(
        text = "Kerakli tugmani tanlang: ",
        reply_markup= action_kb,
    )
    await callback.answer()
    
@action_router.message(F.text == "Menu")
async def show_menu(message:Message):
    await message.answer_photo(
        photo="https://icebergdriveinn.com/cdn/shop/articles/Fast-Food-How-It-Has-Evolved-in-the-Past-Decades.jpg?v=1625683335",
        caption = "Iltimos kerakli fast food ni tanlang",
        reply_markup=await inline_keyboard_menu()
    )
    
@action_router.callback_query(F.data.startswith('food'))
async def show_one_food(callback:CallbackQuery):
    id = int(callback.data.split('_')[1])
    food = get_specific_food(id)
    print(food)
    if food[2].startswith("AgACAgIAAxkBAA"):  
        media = InputMediaPhoto(media=food[2], caption=f'Bu {food[1]}')
    else:
        image = FSInputFile(food[2])
        media = InputMediaPhoto(media=image, caption=f'Bu {food[1]}')
    await callback.message.edit_media(media=media)
    await callback.message.edit_reply_markup(reply_markup=await one_food_inline_button())
    await callback.answer()
    

@action_router.callback_query(F.data.startswith('minus'))
async def minus_food(callback:CallbackQuery):
    quantity = int(callback.data.split('_')[1])
    quantity -= 1
    if quantity >= 1:
        await callback.message.edit_reply_markup(reply_markup=await one_food_inline_button(quantity))
    else:
        await callback.answer("Taom soni 1 dan kam bo'lmaydi!!!")
        
        
        
@action_router.callback_query(F.data.startswith('plus'))
async def plus_food(callback:CallbackQuery):
    quantity = int(callback.data.split('_')[1])
    quantity += 1
    if quantity <= 10:
        await callback.message.edit_reply_markup(reply_markup=await one_food_inline_button(quantity))
    else:
        await callback.answer("Taom soni 10 dan ko'p bo'lmaydi!!!")

    
    
@action_router.callback_query(F.data == 'back')
async def back_to_menu(callback:CallbackQuery):
    pass
    
# @action_router.message()
# async def nothng(message:Message):
#     await message.answer(f"{message.from_user.id}")