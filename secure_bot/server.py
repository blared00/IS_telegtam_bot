import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand
from aiogram.utils import executor
from create_bot import dp
from handler import (handlers_welcome, handlers_test, handlers_game, handlers_main)

"""Логирование"""
logging.basicConfig(level=logging.DEBUG)


async def set_commands(dispatcher: Dispatcher):
    """Функция регистрации команд бота, при его запуске.
    ______
    :param dispatcher.
    """
    await dispatcher.bot.set_my_commands([
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/re", description="Рестарт"),
    ])


async def on_startup(dispatcher: Dispatcher):
    """Функция регистрации  хэндлеров бота, при его запуске.
    ______
    :param dispatcher.
    """
    await set_commands(dispatcher)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
