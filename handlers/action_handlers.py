from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

action_router = Router()

@action_router.message(F.data.in_(['action']))
async def start_action(callback:CallbackQuery):
    pass