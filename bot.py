import asyncio

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

event_loop = asyncio.get_event_loop()