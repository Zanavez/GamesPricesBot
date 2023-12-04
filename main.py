import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from models import connect_to_server

from bot import bot, event_loop


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    connect_task = asyncio.create_task(connect_with_ids())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await connect_task


async def connect_with_ids():
    tasks = []
    with open("user_ids.txt", "r") as f:
        for line in f.readlines():
            tasks.append(connect_to_server(line))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
