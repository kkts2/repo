import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
import database as db
from admin import admin_router
from user import user_router
from soft import soft_router

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(admin_router)
dp.include_router(user_router)
dp.include_router(soft_router)


# Запуск бота
async def main():
    await db.init_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
