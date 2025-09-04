from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .buttons import phone_kb, location_kb, action_kb

register_router = Router()

class Register(StatesGroup):
    fullname = State()
    phone = State()
    loaction = State()


@register_router.message(F.text == "Register")
async def start_register(message:Message, state:FSMContext):
    await state.set_state(Register.fullname)
    await message.answer(
        text = "F.I.Sh kiritng: "
    )

@register_router.message(Register.fullname)
async def get_fullname(message:Message, state:FSMContext):
    text = message.text
    await state.update_data(fullname = text)
    await state.set_state(Register.phone)
    await message.answer(
        text = "Telefon raqamingizni kiritng: ",
        reply_markup=phone_kb
    )

@register_router.message(Register.phone)
async def get_phone(message:Message, state:FSMContext):
    text = message.contact.phone_number
    await state.update_data(phone = text)
    await state.set_state(Register.loaction)
    await message.answer(
        text = "Location jo'nating: ",
        reply_markup=location_kb
    )
    
@register_router.message(Register.loaction)
async def get_location(message:Message, state:FSMContext):
    long = message.location.longitude
    lat = message.location.latitude
    await state.update_data(long = long)
    await state.update_data(lat = lat)
    data = await state.get_data()
    await message.answer(
        text = f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n{data}",
        reply_markup=action_kb
    )