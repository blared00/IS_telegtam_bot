from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import TOKEN


storage = MemoryStorage()

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=storage)