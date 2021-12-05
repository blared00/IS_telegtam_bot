from aiogram.utils.exceptions import TelegramAPIError

import async_db
import markup
import liters
from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp
from utils import BotState, call_main


@dp.callback_query_handler(
    lambda c: c.data == 'main_level',
    state=BotState.MAIN,
)
async def main_(callback_query: types.CallbackQuery):
    """Возвращает в главное меню с удалением всех предыдущих сообщений кроме закрепленного
     _____
    Кнопки:
    Срабатывание - 'Обучение','Опрос' (временно)
    Создает - 'Вернуться в главное меню'."""
    await callback_query.answer()
    await callback_query.message.edit_text(
        liters.CURRENT_LEVEL,
        reply_markup=markup.INLINE_KB_BACKMENU,
    )


@dp.callback_query_handler(
    lambda c: c.data == "back_main_btn",
    state=(
        BotState.MAIN,
        BotState.GAME,
        BotState.NEWLESSON,
    ),
)
async def main_menu_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Возвращает в главное меню с удалением всех предыдущих сообщений кроме закрепленного
     _____
    Кнопки:
    Срабатывание - 'Вернуться в главное меню'
    Создает - главное меню('Тестирование','Обучение',)."""
    await BotState.MAIN.set()
    await callback_query.answer()
    try:
        await callback_query.message.edit_text(
            liters.MAIN_MENU,
            reply_markup=markup.INLINE_KB_MAIN,
        )
    except TelegramAPIError:
        await callback_query.message.delete()
        new_mes = await callback_query.bot.send_message(
            callback_query.from_user.id,
            liters.MAIN_MENU,
            reply_markup=markup.INLINE_KB_MAIN,
        )
        await state.update_data(first_message=new_mes.message_id)
        await async_db.insert_or_update_main(
            callback_query.from_user.id,
            new_mes.message_id,
            state=await state.get_data(),
        )


@dp.message_handler(
    commands=["main", "start"],
    state=(
        BotState.MAIN,
        BotState.GAME,
    ),
)
async def call_main_menu(message: types.Message):
    """Выдает главное меню пользователю
    _____
    Кнопки:
    Создает - главное меню('Поиграем?','Помощь','Обучение','Опрос')."""
    await message.delete()
    await call_main(message.chat.id)
