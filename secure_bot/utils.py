from time import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageToDeleteNotFound,
    MessageToEditNotFound,
    MessageNotModified,
    BotBlocked,
    TelegramAPIError,
    MessageCantBeDeleted,
    CantParseEntities,
)
from django.db.models import QuerySet
from loguru import logger

import async_db

try:
    import async_db
    import liters
    import markup
    from create_bot import dp, storage
    from create_bot import loop
    from settings import BASE_DIR
except ModuleNotFoundError:
    from secure_bot import async_db
    from secure_bot import liters
    from secure_bot import markup
    from secure_bot.create_bot import dp, storage
    from secure_bot.create_bot import loop
    from secure_bot.settings import BASE_DIR
from aiogram.dispatcher.filters.state import State, StatesGroup


class BotState(StatesGroup):
    """Класс состояний бота."""

    STATE_0 = State()
    JOIN_NAME = State()
    ACCEPT_NAME = State()
    EDUCATION = State()
    GAME = State()
    MAIN = State()
    NEWLESSON = State()


async def delete_main_message(user_id: int, main_id: int):
    """Удаление главного сообщения."""
    try:
        await dp.bot.delete_message(chat_id=user_id, message_id=main_id)
    except (MessageToDeleteNotFound, MessageCantBeDeleted) as e:
        logger.add(
            "file_1.log",
        )
        logger.info(f"{e} for telegram user {user_id}. Please, try again.")
        logger.remove()


async def create_pin_message(user_id: int, main_id: int) -> types.Message:
    """Создание закрепленного сообщения"""
    try:

        text_pin = await async_db.get_pin_message()
    except KeyError:
        text_pin = liters.WELCOME3
    await delete_main_message(user_id, main_id)
    mes = await dp.bot.send_message(
        chat_id=user_id,
        text=text_pin[0][0],
        parse_mode=types.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    await dp.bot.pin_chat_message(user_id, mes.message_id)
    return mes


async def call_main(user_id: int):
    """Вызов главного меню"""
    request_state = await async_db.select_state(user_id=user_id)
    _, main_id, _, state = request_state[0]
    if state in ("BotState:MAIN", "BotState:GAME"):
        await BotState.MAIN.set()
        try:
            await dp.bot.edit_message_text(
                chat_id=user_id,
                message_id=main_id,
                text=liters.MAIN_MENU,
                reply_markup=markup.INLINE_KB_MAIN,
            )
        except (MessageNotModified, MessageToEditNotFound):
            await delete_main_message(user_id=user_id, main_id=main_id)
            mes = await dp.bot.send_message(
                chat_id=user_id,
                text=liters.MAIN_MENU + " ",
                reply_markup=markup.INLINE_KB_MAIN,
            )
            await async_db.insert_or_update_main(
                user_id=user_id, main_id=mes.message_id
            )
            return main_id


def edit_pin_message(user_list: QuerySet, text: str):
    """Исправление закрепленного сообщения."""
    for user in user_list:
        if user.pin_message_id:
            try:
                # Исправить закрепленное сообщение
                loop.run_until_complete(
                    dp.bot.edit_message_text(
                        chat_id=int(user.member_id),
                        message_id=int(user.pin_message_id),
                        text=text,
                        parse_mode=types.ParseMode.MARKDOWN,
                        disable_web_page_preview=True,
                    )
                )
            except MessageToEditNotFound:

                # Если было удалено, то удалить главное сообщение, прислать новое сообщение, прислать главное меню
                loop.run_until_complete(
                    delete_main_message(
                        user_id=user.member_id, main_id=user.main_message_id
                    )
                )

                main_id = loop.run_until_complete(call_main(user_id=user.member_id))
                pin = loop.run_until_complete(
                    dp.bot.send_message(
                        chat_id=int(user.member_id),
                        text=text,
                        parse_mode=types.ParseMode.MARKDOWN,
                        disable_web_page_preview=True,
                    )
                )
                state = FSMContext(storage, user=user.member_id, chat=user.member_id)
                loop.run_until_complete(
                    state.update_data(first_message=main_id.message_id)
                )
                loop.run_until_complete(
                    async_db.insert_or_update_state(
                        user_id=user.member_id, main_id=main_id, pin_id=pin.message_id
                    )
                )


async def valid_parse_mode(func, *args, **kwargs):
    """Валидация по методу парсинга сообщения"""
    try:
        result = await func(*args, **kwargs)
    except CantParseEntities:
        kwargs["parse_mode"] = None
        result = await func(*args, **kwargs)
    return result
