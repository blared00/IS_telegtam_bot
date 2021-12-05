import random

from aiogram.utils.exceptions import TelegramAPIError

import async_db
import markup
import liters
from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp
from settings import BASE_DIR
from utils import BotState, delete_main_message


@dp.callback_query_handler(
    lambda c: c.data == "main_game",
    state=(BotState.MAIN, BotState.GAME),
)
async def choise_title(callback_query: types.CallbackQuery):
    """Запускает выбор темы вопросов
        _____
        Кнопки:
        Срабатывание - "Пройти тестирование"
        Создает - Кнопки тем вопросов
        """
    await callback_query.answer()
    await callback_query.message.edit_text(
        liters.MAIN_TEST_MENU,
        reply_markup=markup.INLINE_KB_MAIN_TEST
    )


@dp.callback_query_handler(
    lambda c: c.data in [kb[1] for kb in markup.MAIN_TEST_KB],
    state=(BotState.MAIN, BotState.GAME),
)
async def start_game(callback_query: types.CallbackQuery, state: FSMContext):
    """Запускает случайный вопрос из общего списка, исключая уже заданные
    _____
    Кнопки:
    Срабатывание - "Пройти тестирование", "Ещё?"
    Создает - Кнопки вариантов ответа на вопрос.
    """

    request_question = await random_question(callback_query.from_user.id)
    try:
        new_mes, options, haspicture, description = request_question
        await state.update_data(
            first_message=new_mes.message_id,
            haspicture=haspicture,
            options=tuple(map(lambda x: tuple(x), options)),
            description=description
        )
        await BotState.GAME.set()
    except (ValueError, TypeError):
        new_mes = await callback_query.message.edit_text(
            liters.NO_NEW_QUESTION,
            reply_markup=markup.INLINE_KB_BACKMENU,
        )
        await state.update_data(
            first_message=new_mes.message_id,

        )
    await async_db.insert_or_update_main(
        user_id=callback_query.from_user.id,
        main_id=new_mes.message_id,
        state=await state.get_state(),
    )


async def random_question(user_id: int):
    """
    Достает рандомный вопрос из БД , исключая уже заданные этому пользователю,
    и отправляет.

    :param user_id - id пользователя, которому отправится вопрос
      _____
    Кнопки:
    Срабатывание - "Тестирование", "Далее"
    Создает - Кнопки вариантов ответа на вопрос.
    """

    request_question = await async_db.select_game_question(user_id=user_id)

    if request_question:
        question, options = request_question
        keyboard = markup.range_inline_kb(
            len(options), postfix="g", options=[o for _, o, _ in options], row_size=1
        )
        question_id, question_text, photo, cash, description = question
        user = await async_db.select_state(
            user_id=user_id
        )
        user_id, main_message, _, state_user = user[0]
        await delete_main_message(user_id, main_message)
        if not photo:
            new_mes = await dp.bot.send_message(
                user_id,
                question_text,
                reply_markup=keyboard,
            )
            haspicture = False
        else:
            new_mes = await send_photoquestion(
                user_id,
                question_id,
                question_text,
                photo,
                cash,
                keyboard,
            )
            haspicture = True
        return new_mes, options, haspicture, description
    return None


async def send_photoquestion(
    user_id: int, question_id: int, question_text: str, photo: str, cash: str, keyboard
) -> types.Message:
    """Отправка сообщения с фотографией. Если данное фото уже отправлялось в телеграм боте,
    то вызвать из кэша телеграмма"""
    if cash is not None:
        new_mes = await dp.bot.send_photo(
            user_id,
            photo=cash,
            caption=question_text,
            reply_markup=keyboard,
        )
    else:
        try:
            new_mes = await dp.bot.send_photo(
                user_id,
                photo=open(BASE_DIR / "django_admin/static/{}".format(photo), "rb"),
                caption=question_text,
                reply_markup=keyboard,
            )
            await async_db.insert_cash_photoquestion(
                question_id=question_id, cash=new_mes.photo[0]["file_id"]
            )
        except TelegramAPIError:
            new_mes = await dp.bot.send_message(
                user_id,
                text="Упс вопрос сломался",
                reply_markup=markup.INLINE_KB_BACKGAME,
            )
            await async_db.delete_bag_question(question_id=question_id)
    return new_mes


@dp.callback_query_handler(
    lambda c: c.data in map(lambda x: str(x) + "g", range(1, 6)),
    state=(BotState.MAIN, BotState.GAME),
)
async def answer_question_game(callback_query: types.CallbackQuery, state: FSMContext):
    """Выдает результат при ответе на вопрос. В случае верного ответа поздравит,
    неверного - скажет какой был правильный
    _____
    Кнопки:
    Срабатывание - Кнопки вариантов ответа на вопрос
    Создает -  "Ещё?", "В главное меню".
    """
    user_data = await state.get_data()
    answer = user_data["options"][int(callback_query.data.replace("g", "")) - 1]
    true_answer = [o for o in user_data["options"] if o[2]]
    await async_db.insert_game_answer(user_id=user_data["user_id"], option_id=answer[0])
    await callback_query.message.delete()
    if answer[2]:
        new_mes = await callback_query.bot.send_message(
            callback_query.message.chat.id,
            random.choice(liters.TRUE_ANSWER).capitalize() +f'\n{user_data["description"]}',
            reply_markup=markup.INLINE_KB_BACKGAME,
        )
    else:
        new_mes = await callback_query.bot.send_message(
            callback_query.message.chat.id,
            random.choice(liters.FALSE_ANSWER).capitalize() + "\n" + true_answer[0][1]+f'\n{user_data["description"]}',
            reply_markup=markup.INLINE_KB_BACKGAME,
        )
    await async_db.insert_or_update_main(
        user_id=callback_query.from_user.id,
        main_id=new_mes.message_id,
        state=await state.get_state(),
    )
    await state.update_data(first_message=new_mes.message_id, haspicture=False)
    await BotState.MAIN.set()
