
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from database import conn

scheduler = AsyncIOScheduler()

def setup_scheduler(bot: Bot):
    async def send_reminders():
        # Тут можно выбрать события и отправлять напоминания
        pass

    scheduler.add_job(send_reminders, "interval", minutes=1)
    scheduler.start()
