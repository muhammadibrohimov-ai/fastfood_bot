import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env

from handlers import user_router, admin_router

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher(
        storage=MemoryStorage()
    )
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot,)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Bot stopped with error:\n{e}')