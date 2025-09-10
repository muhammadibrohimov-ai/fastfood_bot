from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from .buttons import admin_kb, registered_kb, add_foods, inline_keyboard_foods

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database import add_to_table

from environs import Env
env = Env()
env.read_env()

ADMIN_ID = env.str("ADMIN")

admin_router = Router()

class Register_food(StatesGroup):
    name = State()
    image = State()
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
            text = "Admin Paelga xush kelibsiz!\nKerakli tugamni tang=lang: ",
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
        await state.set_state(Register_food.price)
        await message.answer(
            text = f'{photo_id}\nIltimos taom narxini kiriting: '
        )
        
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
    if add_to_table('foods', name = data['name'], price = data['price'], image = data['image'], quantity = data['quantity']):
        await message.answer(
            text = f"Taom database ga qo'shildi!\n{data}"
        )
        
    else:
        await message.answer(
            text = "Xatolik ketdi qayta urining\nQuyidagilardan birini tanlang: ",
            reply_markup=add_foods
        )
    
    