import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

try:
    import settings
except ModuleNotFoundError:
    from secure_bot import settings


storage = MemoryStorage()

bot = Bot(token=settings.TOKEN)

dp = Dispatcher(bot, storage=storage)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot_name = loop.run_until_complete(bot.get_me())['username']
