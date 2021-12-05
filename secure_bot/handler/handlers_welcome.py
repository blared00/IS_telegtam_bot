from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

import async_db
import markup
import liters
from utils import BotState
from create_bot import dp


@dp.message_handler(commands=["start"])
async def start_messages(message: types.Message, state: FSMContext):
    """Приветствие пользователя
    ______
    Кнопки:
    -Привет.
    """
    args = message.get_args()

    if args == "Pzs6_Gxa":
        new_mes = await message.answer(
            liters.WELCOME1,
            reply_markup=markup.INLINE_KB_WELCOME,
        )
        await message.delete()
        await state.update_data(first_message=new_mes.message_id)
        await BotState.STATE_0.set()
    else:
        await message.answer(
            "У Вас нет доступа для связи с ботом, либо данный пользователь уже зарегистрирован"
        )


@dp.callback_query_handler(
 lambda c: c.data == "welcome_btn", state=BotState.STATE_0
    )
async def welcome(callback_query: types.CallbackQuery):
    """Реакция на команду с клавиши "Привет"
    _____
    Кнопки:
    Срабатывание - "Привет"
    _____
    Переход в состояние Join_name."""
    await callback_query.answer(text="Мы рады, что ты начал обучение")
    await callback_query.message.edit_text(liters.NAME_QUESTION)
    await BotState.JOIN_NAME.set()


@dp.message_handler(state=BotState.JOIN_NAME)
async def request_name(message: types.Message, state: FSMContext):
    """Запись имени пользователя.
    ____
    Кнопки:
    Создает - "Конечно", "Начать с азов".
    """
    name = message.text
    await async_db.insert_user(
        user_id=message.from_user.id,
        user_name=name.title(),
        user_name_tg=message.from_user.username,
    )

    await state.update_data(
        user_name=name.title(),
        user_name_tg=message.from_user.username,
        tg_user_id=message.from_user.id,
        user_id=message.from_user.id,
        answer_question_game=[],
    )
    await message.delete()
    user_data = await state.get_data()
    await message.bot.edit_message_text(
        liters.NAME_ACCEPT.format(name.title()),
        message.from_user.id,
        user_data["first_message"],
        reply_markup=markup.INLINE_KB_FACT,
    )
    await async_db.insert_or_update_main(
        user_id=message.from_user.id, main_id=user_data["first_message"]
    )
    await BotState.ACCEPT_NAME.set()


@dp.message_handler(commands=["re"], state="*")
async def restart(message: types.Message, state: FSMContext):
    """Перезагружает скрипт (функция для разработки)."""
    user_data = await state.get_data()
    await message.delete()
    await state.reset_state()
    try:
        await dp.bot.delete_message(
            message.chat.id, message_id=user_data["first_message"]
        )
    except (MessageToDeleteNotFound, MessageCantBeDeleted):
        pass
    except KeyError:
        return
    await async_db.del_user(message.from_user.id)


@dp.message_handler(
    state=(
        BotState.STATE_0,
        BotState.ACCEPT_NAME,
        BotState.GAME,
    ),
)
async def del_waste(message: types.Message):
    """Удаляет сообщения пользователя , когда он не должен писать"""
    await message.delete()
