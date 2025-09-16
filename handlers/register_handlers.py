from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .check import check_phone, location_check

from .buttons import phone_kb, location_kb, action_ikb, register_kb
from database import add_to_table

from environs import Env
env = Env()
env.read_env()

ADMIN_ID = env.str("ADMIN")

register_router = Router()

class Register(StatesGroup):
    fullname = State()
    phone = State()
    loaction = State()


@register_router.message(F.text == "Register")
async def start_register(message:Message, state:FSMContext):
    await state.set_state(Register.fullname)
    await state.update_data(chat_id = message.from_user.id)
    await state.update_data(username = message.from_user.username)
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
    if message.contact:
        text = message.contact.phone_number
        status = True
        
    else:
        text = message.text
        status = await check_phone(text)
        
    if not status:
        await message.answer(
            text = "Telefon raqamingizni qayta yuboring: ",
            reply_markup=phone_kb
        )
    else:
        await state.update_data(phone = text)
        await state.set_state(Register.loaction)
        await message.answer(
            text = "Location jo'nating: ",
            reply_markup=location_kb
        )

    
    
@register_router.message(Register.loaction)
async def get_location(message:Message, state:FSMContext):
    status_1 = True
    status_2 = True
    status_3 = True
    if message.forward_origin:
        status_1 = False
    
    try:
        long = message.location.longitude
        lat = message.location.latitude
        
    except:
        status_2 = False
    
    status_3 = await location_check(latitude=lat, longitude=long)

    if not (status_1 and status_2 and status_3):
        await message.answer(
            text = "Location qayta jo'nating: ",
            reply_markup=location_kb
        )
    else:
        await state.update_data(long = long)
        await state.update_data(lat = lat)
        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{long}"

        await state.update_data(location_link=maps_url)
        
        data = await state.get_data()
        await state.clear()
    

        if add_to_table('users', chat_id=data['chat_id'], username = data['username'], fullname=data['fullname'], long = data['long'], lat = data['lat'], is_admin = 'true' if str(message.from_user.id) == str(ADMIN_ID) else 'false', phone = data['phone'], location_link = data['location_link']):
            await message.answer(
                text = f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n{data}\n\n{maps_url}",
                reply_markup=action_ikb
            )
        else:
            await message.answer(
                text = 'Xatolik yuz berdi , iltimos qayta urining!',
                reply_markup=register_kb
            )