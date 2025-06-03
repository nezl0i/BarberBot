from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    try:
        for ADMIN_ID in settings.ADMIN_IDS:
            await bot.send_message(ADMIN_ID, f'Я запущен🥳.')
    except (Exception,):
        pass


async def stop_bot():
    try:
        for ADMIN_ID in settings.ADMIN_IDS:
            await bot.send_message(ADMIN_ID, 'Бот остановлен. За что?😔')
    except (Exception,):
        pass