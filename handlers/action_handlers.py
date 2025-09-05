from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .buttons import action_kb

action_router = Router()

@action_router.callback_query(F.data.in_(['action',]))
async def start_action(callback:CallbackQuery):
    await callback.message.answer(
        text = "Kerakli tugmani tanlang: ",
        reply_markup= action_kb,
    )
    await callback.answer()