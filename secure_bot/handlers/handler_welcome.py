from aiogram import types
from aiogram.dispatcher import FSMContext

from secure_bot import liters, markup
from secure_bot.create_bot import dp
from secure_bot.utils import BotState


@dp.message_handler(commands=["start"])
async def start_messages(message: types.Message, state: FSMContext):
    """Приветствие пользователя
    ______
    Кнопки:
    -Привет!
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
    """Реакция на команду с клавиши Привет, Марта
    _____
    Кнопки:
    Срабатывание - "Привет, Марта"
    _____
    Переход в состояние Join_name."""
    await callback_query.answer()
    await callback_query.message.edit_text(liters.NAME_QUESTION)
    await BotState.JOIN_NAME.set()
