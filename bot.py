
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import event
from scheduler import setup_scheduler

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(event.router)
    setup_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
