import async_db
import markup
import liters
from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp
from utils import BotState, POLL_STATE, CONNECT_POLL, create_pin_message


@dp.callback_query_handler(
    lambda c: c.data == 'back_main_btn',
    state=BotState.ACCEPT_NAME,
)
async def go_to_mainmenu(callback_query: types.CallbackQuery, state: FSMContext):
    mes = await create_pin_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    new_mes = await callback_query.bot.send_message(
        callback_query.message.chat.id,
        liters.MAIN_MENU,
        reply_markup=markup.INLINE_KB_MAIN,
    )
    await async_db.insert_or_update_state(
        user_id=callback_query.from_user.id,
        pin_id=mes.message_id,
        main_id=new_mes.message_id,
        state="BotState:MAIN",
    )

    await state.update_data(
        first_message=new_mes.message_id, pin_message=mes.message_id
    )


@dp.callback_query_handler(
    lambda c: c.data == '2_6_week',
    state=BotState.ACCEPT_NAME,
)
async def how_long_work(callback_query: types.CallbackQuery, state: FSMContext):
    """Начинает опрос в соответствии с выбранным вариантом ответа
    _____
    Кнопки:
    Срабатывание - "Конечно"
    Создает - 1 вопрос из POLL№ в соответствии с выбранным вариантом ответа на вопрос "Как долго работаешь?"
    _____
    Переходит в состояние POLL№.
    """
    await callback_query.answer()
    await state.update_data(how_long_work=callback_query.data)
    poll_id = CONNECT_POLL[callback_query.data]
    poll = await async_db.select_poll(poll_id=poll_id)
    question_id, poll_first_question, count_key, key_options, text_answer = poll[0]
    await callback_query.message.edit_text(
        poll_first_question.capitalize(),
        reply_markup=markup.range_inline_kb(count_key, "p", key_options.split(";")),
        parse_mode=types.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    await state.update_data(poll_question=0, poll=tuple(map(lambda x: tuple(x), poll)), poll_id=poll_id)
    await POLL_STATE[callback_query.data].set()


@dp.callback_query_handler(
    lambda c: c.data in map(lambda x: str(x) + "p", range(1, 6)),
    state=(BotState.POLL1, BotState.POLL2, BotState.POLL3),
)
async def poll_func_kb(callback_query: types.CallbackQuery, state: FSMContext):
    """Записывает результат ответа на предыдущий вопрос в БД , выдает новый вопрос.
    Если Вопрос последний, то переводит в состояние MAIN.
     _____
    Кнопки:
    Срабатывание - Кнопки опросов (1, 2, 3 и т.д)
    Создает - Новый вопрос по списку.
    """
    await callback_query.bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await async_db.insert_answer(
        user_id=user_data["user_id"],
        question_id=user_data["poll"][user_data["poll_question"]][0],
        answer=callback_query.data.replace("p", ""),
    )
    await state.update_data(
        poll_question=user_data["poll_question"] + 1,
    )
    user_data = await state.get_data()

    try:
        question_id, question, count_key, key_options, text_answer = user_data["poll"][
            user_data["poll_question"]
        ]
        await callback_query.message.edit_text(
            question,
            reply_markup=markup.range_inline_kb(count_key, "p", key_options.split(";")),
            parse_mode=types.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )

    except IndexError:
        await async_db.insert_poll_answer(
            user_id=user_data["user_id"], poll_id=user_data["poll_id"]
        )
        mes = await create_pin_message(
            callback_query.message.chat.id, callback_query.message.message_id
        )
        new_mes = await dp.bot.send_message(
            callback_query.from_user.id,
            text=liters.CONGRATULATION + "\n\n" + liters.MAIN_MENU,
            reply_markup=markup.INLINE_KB_MAIN,
        )

        await BotState.MAIN.set()
        await async_db.insert_or_update_state(
            user_id=callback_query.from_user.id,
            main_id=new_mes.message_id,
            pin_id=mes.message_id,
            state="BotState:MAIN",
        )
        await state.update_data(
            first_message=new_mes.message_id, pin_message=mes.message_id
        )


@dp.message_handler(state=(BotState.POLL1, BotState.POLL2, BotState.POLL3))
async def poll_func_ms(message: types.Message, state: FSMContext):
    """Записывает текст сообщения как ответ, если вопрос подразумевает ответ сообщением, если нет, то удаляет
    сообщение пользователя"""
    user_data = await state.get_data()
    if user_data["poll"][user_data["poll_question"]][4]:
        await async_db.insert_answer(
            user_id=user_data["user_id"],
            question_id=user_data["poll"][user_data["poll_question"]][0],
            answer=message.text,
        )
        await state.update_data(
            poll_question=user_data["poll_question"] + 1,
        )
        user_data = await state.get_data()
        try:
            question_id, question, count_key, key_options, text_answer = user_data[
                "poll"
            ][user_data["poll_question"]]
            await message.bot.edit_message_text(
                question,
                message.from_user.id,
                user_data["first_message"],
                reply_markup=markup.range_inline_kb(
                    count_key, "p", key_options.split(";")
                ),
                parse_mode=types.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
            await message.delete()
        except IndexError:
            await async_db.insert_poll_answer(
                user_id=user_data["user_id"], poll_id=user_data["poll_id"]
            )
            mes = await create_pin_message(message.chat.id, message.message_id)
            new_mes = await dp.bot.send_message(
                message.chat.id,
                text=liters.CONGRATULATION + "\n\n" + liters.MAIN_MENU,
                reply_markup=markup.INLINE_KB_MAIN,
            )

            await BotState.MAIN.set()
            await async_db.insert_or_update_state(
                user_id=message.chat.id,
                main_id=new_mes.message_id,
                pin_id=mes.message_id,
                state="BotState:MAIN",
            )
            await state.update_data(
                first_message=new_mes.message_id, pin_message=mes.message_id
            )
            await message.delete()
            await async_db.insert_or_update_main(
                user_id=message.from_user.id,
                main_id=user_data["first_message"],
                state=await state.get_state(),
            )
    else:
        await message.delete()
