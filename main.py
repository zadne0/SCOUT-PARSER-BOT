import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers.common import router as common_router 
from handlers.scout import router as scout_router

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры (наши обработчики)
    dp.include_router(scout_router)
    dp.include_router(common_router)

    print("Разведчик заступил на дежурство!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Разведчик ушел в тень.")