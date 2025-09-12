import asyncio

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

from .buttons import action_kb, inline_keyboard_menu, one_food_inline_button, send_cancel_food
from database import get_specific_food, add_to_table, get_users, change_table


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
    await callback.message.edit_reply_markup(reply_markup=await one_food_inline_button(id))
    await callback.answer()
    

@action_router.callback_query(F.data.startswith('minus'))
async def minus_food(callback:CallbackQuery):
    food_id = int(callback.data.split('_')[-1])
    quantity = int(callback.data.split('_')[1])
    quantity -= 1
    if quantity >= 1:
        await callback.message.edit_reply_markup(reply_markup=await one_food_inline_button(food_id, quantity))
    else:
        await callback.answer("Taom soni 1 dan kam bo'lmaydi!!!")
        
        
        
@action_router.callback_query(F.data.startswith('plus'))
async def plus_food(callback:CallbackQuery):
    food_id = int(callback.data.split('_')[-1])
    quantity = int(callback.data.split('_')[1])
    quantity += 1
    if quantity <= 10:
        await callback.message.edit_reply_markup(reply_markup=await one_food_inline_button(food_id, quantity))
    else:
        await callback.answer("Taom soni 10 dan ko'p bo'lmaydi!!!")

    
@action_router.callback_query(F.data.startswith("order"))
async def show_order(callback:CallbackQuery):
    quantity = int(callback.data.split('_')[1])
    food_id = int(callback.data.split('_')[-1])
    user_id = int(callback.from_user.id)
    food = get_specific_food(food_id)
    await callback.message.edit_caption(
        caption= f"""
        🍽 Taom: {food[1]}
💵 Narxi: {food[3]},000 so'm
📦 Soni: {quantity} ta

💵 Umumiy: {quantity * food[3]} so'm
Siz ushbu buyurtmani tasdiqlaysizmi?
        """,
        reply_markup=await send_cancel_food(quantity, food_id)
    )
    
@action_router.callback_query(F.data.startswith('send'))
async def send_to_db(callback:CallbackQuery):
    quantity = int(callback.data.split('_')[1])
    food_id = int(callback.data.split('_')[-1])
    user_chat_id = int(callback.from_user.id)
    user_id = get_users(user_chat_id)[0]
    food = get_specific_food(food_id)
    if add_to_table('orders', food_id = food_id, user_id = user_id, quantity = quantity, price = str(food[3]), status = 'new'):
        await callback.message.delete()
        
        await callback.message.answer(
            text="Iltimos kerakli buyruqni tanlang:",
            reply_markup=action_kb
        )
        
        await asyncio.sleep(3)
        
        print(change_table(f"UPDATE orders SET status = 'finished' WHERE user_id = {user_id}"))
    
    
@action_router.callback_query(F.startswith('back'))
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media="https://icebergdriveinn.com/cdn/shop/articles/Fast-Food-How-It-Has-Evolved-in-the-Past-Decades.jpg?v=1625683335",
            caption="Iltimos kerakli taomni tanlang:"
        )
    )

    await callback.message.edit_reply_markup(reply_markup=await inline_keyboard_menu())
   
   


# @action_router.message()
# async def nothng(message:Message):
#     await message.answer(f"{message.from_user.id}")