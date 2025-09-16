from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .buttons import admin_kb, registered_kb, add_foods, inline_keyboard_foods, order_show, order_inline_kb

from database import add_to_table, get_order_food, change_table

from environs import Env
env = Env()
env.read_env()

ADMIN_ID = env.str("ADMIN")

admin_router = Router()

class Register_food(StatesGroup):
    name = State()
    image = State()
    decription = State()
    price = State()
    quantity = State()
    
class Edit_food(StatesGroup):
    start = State()
    feature = State()

@admin_router.message(Command("admin"))
async def start_admin(message:Message):
    id = str(message.from_user.id)
    if str(ADMIN_ID) == id:
        await message.answer(
            text = 
            "🎛 <b>Admin Panel</b> ga xush kelibsiz!\n\n"
        "Quyidagi bo‘limlardan birini tanlang:\n\n"
        "🍽 Taom qo‘shish\n"
        "🛒 Buyurtmalar\n"
        "💬 Xabarlar\n"
        "👤 User panelga qaytish",
            reply_markup=admin_kb
        )
    else:
        await message.answer(
            text = "Siz admin emasssiz, iltimos kerakli tugmani tanlang: ",
            reply_markup=registered_kb
        )
        
@admin_router.message(F.text == 'Taom qo\'shish')
async def add_food(message:Message):
        await message.answer(
            text = "Quyidagilardan birini tanlang: ",
            reply_markup=add_foods
        )
    
@admin_router.callback_query(F.data.endswith('food'))
async def choose_which(callback:CallbackQuery, state:FSMContext):
    if callback.data.split('_')[0] == 'new':
        await state.set_state(Register_food.name)
        await callback.message.answer(
            text = "Taom nomini kiring: "
        )
        callback.answer()
        
    else:
        await state.set_state(Edit_food.start)
        await callback.message.answer(
            text = "Iltimos kerakli taomini tanlang: ",
            reply_markup=await inline_keyboard_foods()
        )
        callback.answer()

@admin_router.message(Register_food.name)
async def get_new_food_name(message:Message, state:FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Register_food.image)    
    await message.answer(
        text = "Iltimos taomning rasmini jo'nating"
    )
    
@admin_router.message(Register_food.image)
async def get_new_food_image(message:Message, state:FSMContext):
    if not message.photo:
        await message.answer(
            text = "Iltimos taomning qayta rasmini jo'nating"
        ) 
    
    else:
        photo_id = message.photo[-1].file_id
        await state.update_data(image = photo_id)
        await state.set_state(Register_food.decription)
        await message.answer(
            text = f'{photo_id}\nIltimos taomga sharh yozing: '
        )
        
@admin_router.message(Register_food.decription)
async def get_description(message:Message, state:FSMContext):
    text = message.text
    await state.update_data(description = text)
    await state.set_state(Register_food.price)
    await message.answer("Iltimos taomning narxini kiritng: ")
        
@admin_router.message(Register_food.price)
async def get_new_food_price(message:Message, state:FSMContext):
    await state.update_data(price = message.text)
    await state.set_state(Register_food.quantity)
    await message.answer(
        text = 'Iltimos taomning miqdorini kiritng: '
    )
    

@admin_router.message(Register_food.quantity)
async def get_new_food_quantity(message:Message, state:FSMContext):
    await state.update_data(quantity = message.text)
    data = await state.get_data()
    await state.clear()
    if add_to_table('foods', name = data['name'], price = data['price'], image = data['image'], quantity = data['quantity'], description = data['description']):
        await message.answer(
            text = f"Taom database ga qo'shildi!\n{data}",
            reply_markup=admin_kb
        )
        
    else:
        await message.answer(
            text = "Xatolik ketdi qayta urining\nQuyidagilardan birini tanlang: ",
            reply_markup=add_foods
        )
        
@admin_router.message(F.text == "Buyurtmalar")
async def show_orders(message:Message):
    await message.answer(
        text = 'Qanday turdagi buyurtmalarni ko\'rmoqchisiz, kerakli tugmani bosing: ',
        reply_markup=order_show
    )
    
    
@admin_router.message(F.text == "🆕New")
async def show_new_order(message:Message):
    foods = get_order_food(status='new')
    for i in foods:
        order_id, food_name, user_id, food_price, order_quantity, total_price = i
        await message.answer(
            text = f'🍽 Taom: {food_name}\n💵 Narxi: {food_price:,} so\'m\n📦 Soni: {order_quantity}\n💵 Umumiy: {total_price:,} so\'m\n',
            reply_markup=await order_inline_kb(order_id)
        )    
        
@admin_router.message(F.text == "In progress")
async def show_progress_order(message:Message):
    foods = get_order_food(status='in_progress')
    for i in foods:
        order_id, food_name, user_id, food_price, order_quantity, total_price = i
        await message.answer(
            text = f'🍽 Taom: {food_name}\n💵 Narxi: {food_price:,} so\'m\n📦 Soni: {order_quantity}\n💵 Umumiy: {total_price:,} so\'m\n',
            reply_markup=await order_inline_kb(order_id, 2)
        )    
        
@admin_router.message(F.text == "Finished")
async def show_progress_order(message:Message):
    foods = get_order_food(status='finished')
    for i in foods:
        order_id, food_name, user_id, food_price, order_quantity, total_price = i
        await message.answer(
            text = f'🍽 Taom: {food_name}\n💵 Narxi: {food_price:,} so\'m\n📦 Soni: {order_quantity}\n💵 Umumiy: {total_price:,} so\'m\n',
            reply_markup=await order_inline_kb(order_id, 2)
        )    
        

@admin_router.callback_query(F.data.startswith(('progress', 'finish')))
async def change_order(callback:CallbackQuery):
    status = callback.data.split('_')[0]
    order_id = callback.data.split('_')[1]
    print(order_id)
    if change_table("UPDATE orders SET status = '%s' WHERE id = %s"%('finished' if status == 'finish' else 'in_progress', order_id)):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text = 'Success')

    
