from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from .buttons import admin_kb, registered_kb, add_foods, inline_keyboard_foods

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

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
        state.set_state(Register_food.name)
        await callback.message.answer(
            text = "Taom nomini kiring: "
        )
        await callback.answer()
    else:
        await callback.message.answer(
            text = "Iltimos kerakli taomini tanlang: ",
            reply_markup=await inline_keyboard_foods()
        )
        await callback.answer()
        
        