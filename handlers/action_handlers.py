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

from .check import check_phone, location_check

from .buttons import action_kb, inline_keyboard_menu, one_food_inline_button, send_cancel_food, settings, phone_kb, location_kb
from database import get_specific_food, add_to_table, get_users, change_table, get_user_order, add_comment

class AddComment(StatesGroup):
    comment = State()


action_router = Router()


@action_router.callback_query(F.data == 'main')
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
    media = InputMediaPhoto(media=food[2], caption=f'{food[-1]}')
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
        
        change_table(f"UPDATE foods SET quantity = (quantity - {quantity}) WHERE id = {food_id};")
        
        await callback.message.answer(
            text="Success!!!\nIltimos kerakli buyruqni tanlang:",
            reply_markup=action_kb
        )
        
    
    
        
    
@action_router.callback_query(F.data.startswith('back'))
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media="https://icebergdriveinn.com/cdn/shop/articles/Fast-Food-How-It-Has-Evolved-in-the-Past-Decades.jpg?v=1625683335",
            caption="Iltimos kerakli taomni tanlang:"
        )
    )

    await callback.message.edit_reply_markup(reply_markup=await inline_keyboard_menu())
   
@action_router.message(F.text == 'Buyurtmalarim')
async def user_orders(message: Message):
    user_orders = get_user_order(message.from_user.id)

    if user_orders:
        for order in user_orders:
            order_id, food_name, user_id, food_price, order_quantity, total_price, status, created_at = order

            text = (
                f"📌 Buyurtma ID: {order_id}\n"
                f"🍽 Taom: {food_name}\n"
                f"💵 Narxi: {food_price:,} so'm\n"
                f"📦 Soni: {order_quantity} ta\n"
                f"💰 Umumiy: {total_price:,} so'm\n"
                f"📅 Sana: {created_at}\n"
                f"📊 Holat: {status}\n"
            )

            await message.answer(text=text)
            
    else:
        await message.answer(
            text = """📭 Sizning buyurtmalaringiz ro‘yxati hozircha bo‘sh.  

🍔 Iltimos, ovqatlardan birini tanlab buyurtma qiling!
""",
            reply_markup=action_kb
        )

        
@action_router.message(F.text == "Aloqa")
async def get_comment_from_user(message:Message, state:FSMContext):
    await state.set_state(AddComment.comment)
    await message.answer(
        text = "📩 *Aloqa bo‘limi*\n\n"
            "Adminlar bilan bog‘lanish uchun quyidagi ma’lumotlardan foydalanishingiz mumkin:\n"
            "👤 Admin: @muhammadibrohimovceo\n"
            "📞 Telefon: +998 88 008 45 06\n\n"
            "✍️ Shu yerga o‘z fikr-mulohazalaringiz yoki savollaringizni yozib qoldiring: "
    )
    
@action_router.message(AddComment.comment)
async def get_comment(message: Message, state: FSMContext):
    comment = message.text
    await state.clear()
    
    add_comment(message.from_user.id, comment)
    
    await message.answer(
        text = "✅ Rahmat, adminlarimizga yetkazildi!\n\nIltimos, kerakli tugmani tanlang:",
        reply_markup=action_kb
    )
    
    
    

@action_router.message()
@action_router.message(Command("help"))
@action_router.message(F.text.in_(["Elp", "Yordam", "Help"]))
async def show_help(message: Message):
    help_text = (
        "🆘 <b>Yordam bo‘limi</b>\n\n"
        "Quyidagi komandalar orqali botdan foydalanishingiz mumkin:\n\n"
        "👤 <b>Ro‘yxatdan o‘tish:</b>\n"
        "▫️ Register — ro‘yxatdan o‘tish\n\n"
        "🍔 <b>Buyurtma berish:</b>\n"
        "▫️ Menu yoki /start — menyuni ko‘rish\n"
        "▫️ Buyurtmalarim — buyurtmalaringizni ko‘rish\n\n"
        "📞 <b>Aloqa:</b>\n"
        "▫️ Aloqa — admin bilan bog‘lanish\n\n"
        "🎛 <b>Admin komandalar:</b>\n"
        "▫️ /admin — admin panelga kirish\n\n"
        "ℹ️ Maslahat: komandani /help yozib yuborsangiz, shu oynani qayta ochasiz."
    )
    await message.answer(help_text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=action_kb)
