import logging
from aiogram.utils import executor

from .create_bot import dp


"""Логирование"""
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)