from aiogram.utils.exceptions import TelegramAPIError

import async_db
import markup
import liters
from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp
from utils import BotState, create_pin_message, call_main


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
    await BotState.MAIN.set()
    await state.update_data(
        first_message=new_mes.message_id, pin_message=mes.message_id
    )


@dp.callback_query_handler(
    lambda c: c.data == 'ofcourse_btn',
    state=BotState.ACCEPT_NAME,
)
async def how_long_work(callback_query: types.CallbackQuery, state: FSMContext):
    """Начинает тестирование
    _____
    Кнопки:
    Срабатывание - "Конечно"
    Создает - 1 вопрос из POLL№ в соответствии с выбранным вариантом ответа на вопрос "Как долго работаешь?"
    _____
    Переходит в состояние POLL№.
    """
    await callback_query.answer()
    await state.update_data(how_long_work=callback_query.data)
    questions_list = []
    cat_id = 1
    request_q = await async_db.seclect_cup_question(cat_id)
    if request_q:
        for q in request_q:
            questions_list.append(tuple(q))

    question_id, text, description = tuple(questions_list.pop())
    options = await async_db.seclect_options_question(question_id)
    print(list(map(lambda x: x[1], options)))
    await callback_query.message.edit_text(
        text,
        reply_markup=markup.range_inline_kb(len(options), "g",list(map(lambda x: x[1], options))),
        parse_mode=types.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    await state.update_data(first_test=tuple(map(lambda x: tuple(x), questions_list)))
    await BotState.EDUCATION.set()


@dp.callback_query_handler(
    lambda c: c.data in map(lambda x: str(x) + "g", range(1, 6)),
    state=BotState.EDUCATION
)
async def poll_func_kb(callback_query: types.CallbackQuery, state: FSMContext):
    """Записывает результат ответа на предыдущий вопрос в БД , выдает новый вопрос.
    Если Вопрос последний, то переводит в состояние MAIN.
     _____
    Кнопки:
    Срабатывание - Кнопки опросов (1, 2, 3 и т.д)
    Создает - Новый вопрос по списку.
    """
    await callback_query.answer()
    user_data = await state.get_data()
    question_list =list(user_data['first_test'])
    try:
        question_id, text, description = question_list.pop()
        options = await async_db.seclect_options_question(question_id)
        await callback_query.message.edit_text(
            text,
            reply_markup=markup.range_inline_kb(len(options), "g", list(map(lambda x: x[1], options))),
            parse_mode=types.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        await state.update_data(first_test=question_list)
    except IndexError:
        await BotState.MAIN.set()
        await callback_query.message.delete()
        mes = await create_pin_message(
            callback_query.message.chat.id, callback_query.message.message_id
        )
        new_mes = await callback_query.bot.send_message(
            callback_query.message.chat.id,
            'Ты хорошо отвечал, но все же необходимо подкрепить свои знания для повышения уровня\n' + liters.MAIN_MENU,
            reply_markup=markup.INLINE_KB_MAIN,
        )
        await state.update_data(
            first_message=new_mes.message_id, pin_message=mes.message_id
        )
