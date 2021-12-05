import asyncio
import random

import asyncpg
from datetime import datetime

try:
    import settings
except ModuleNotFoundError:
    from secure_bot import settings

DATABASE = {
    "database": settings.DATABASES["default"]["NAME"],
    "user": settings.DATABASES["default"]["USER"],
    "password": settings.DATABASES["default"]["PASSWORD"],
    "host": settings.DATABASES["default"]["HOST"],
}


def psycopg2_cursor(conn_info):
    """Декоратор для оборачивания функций, работающих с БД."""

    def wrap(f):
        async def wrapper(*args, **kwargs):
            try:
                # Открыть соединение с бд
                connection = await asyncpg.connect(**conn_info)

                # Вызов функции с курсором
                return_val = await f(connection, *args, **kwargs)
            finally:
                # Закрыть соединение
                await connection.close()

            return return_val

        return wrapper

    return wrap


"""Функции с пользователями"""


@psycopg2_cursor(DATABASE)
async def insert_user(conn, user_id: int, user_name: str, user_name_tg: str):
    """Добавление новых пользователей."""
    result = await conn.fetch(
        """SELECT * FROM member WHERE tg_id=$1""",
        user_id,
    )
    if result:
        await del_user(user_id=user_id)
    await conn.execute(
        """INSERT INTO member(tg_id, tg_name, name) VALUES ($1,$2,$3)""",
        user_id,
        user_name_tg,
        user_name,
    )
    await conn.execute(
        """
        INSERT INTO member_score(amount, category_id, member_id) VALUES (0,1,$1)
        """,
        user_id,

    )
    await conn.execute(
        """
        INSERT INTO member_score(amount, category_id, member_id) VALUES (1,2,$1)
        """,
        user_id,

    )
    await conn.execute(
        """
        INSERT INTO member_score(amount, category_id, member_id) VALUES (0,1,$1);
        """,
        user_id,

    )


@psycopg2_cursor(DATABASE)
async def del_user(conn, user_id: int):
    """Удалить данные о пользователе"""

    MEMBER_TABLE_SHIP = (
        "call_support_memberquestion",
        "member_state",
        "poll_questionanswer",
        "poll_answer",
        "game_answer",
    )
    await conn.execute(
        """DELETE FROM call_support_answeroperator USING call_support_memberquestion
         WHERE question_id = call_support_memberquestion.id AND call_support_memberquestion.member_id=$1""",
        user_id,
    )
    for name_table in MEMBER_TABLE_SHIP:
        await conn.execute(
            """DELETE FROM {} WHERE member_id=$1""".format(name_table),
            user_id,
        )
    await conn.execute(
        """DELETE FROM member WHERE tg_id=$1""",
        user_id,
    )


@psycopg2_cursor(DATABASE)
async def select_user(cursor, tg_user_id: int):
    """Получение данных о пользователе."""
    return await cursor.fetchrow(
        """SELECT *
                    FROM member
                    WHERE tg_id = $1""",
        tg_user_id,
    )


@psycopg2_cursor(DATABASE)
async def insert_or_update_main(conn, user_id: int, main_id: int, state: str = None):
    """Добавление или обновление состояния пользователя."""
    await conn.execute(
        """INSERT INTO member_state (member_id, main_message_id, state) VALUES ($1, $2, $3)
        ON CONFLICT (member_id) DO UPDATE SET main_message_id = $2, state = $3""",
        user_id,
        main_id,
        state,
    )


@psycopg2_cursor(DATABASE)
async def select_all_users(connection):
    """Выбрать всех пользователей, чье состояние после MainMenu."""
    result = await connection.fetch(
        """SELECT member_id FROM member_state WHERE state
        IN ('BotState:GAME', 'BotState:HELP', 'BotState:MAIN') """
    )
    if result is None:
        return []
    return result


@psycopg2_cursor(DATABASE)
async def insert_or_update_state(
    conn, user_id: int, main_id: int, pin_id: int, state: str = None
):
    """Добавление или обновление состояния пользователя."""
    await conn.execute(
        """INSERT INTO member_state (member_id, main_message_id, pin_message_id, state) VALUES ($1, $2, $3, $4)
        ON CONFLICT (member_id) DO UPDATE SET main_message_id = $2, pin_message_id = $3, state = $4""",
        user_id,
        main_id,
        pin_id,
        state,
    )


@psycopg2_cursor(DATABASE)
async def select_state(conn, user_id: int):
    """Получить состояние пользователя."""
    return await conn.fetch(
        """SELECT * FROM member_state WHERE member_id = $1
        """,
        user_id,
    )


"""Функции с опросами"""


@psycopg2_cursor(DATABASE)
async def insert_answer(cursor, user_id: int, question_id: int, answer: str):
    """Добавление новых ответов пользователя."""
    await cursor.fetch(
        """INSERT INTO poll_questionanswer(member_id, question_id, answer, date) VALUES ($1,$2,$3,$4)""",
        user_id,
        question_id,
        answer,
        datetime.now(),
    )


@psycopg2_cursor(DATABASE)
async def insert_poll_answer(conn, user_id: int, poll_id: int):
    """Добавление новых ответов пользователя."""
    await conn.execute(
        """INSERT INTO poll_answer(member_id, poll_id, date) VALUES ($1,$2,$3)""",
        user_id,
        poll_id,
        datetime.now(),
    )


@psycopg2_cursor(DATABASE)
async def select_poll(conn, poll_id: int):
    """Получение опроса."""
    return await conn.fetch(
        """SELECT poll_question.id, poll_question.text,
                  poll_questionoptions.count_key,
                  poll_questionoptions.text_key,
                  poll_question.text_answer
                    FROM poll_question
                    INNER JOIN poll_questionoptions ON poll_questionoptions.id = poll_question.options_id
                    WHERE poll_id = $1
                    ORDER BY poll_question.id""",
        poll_id,
    )


@psycopg2_cursor(DATABASE)
async def seclect_cup_question(conn, category: int):
    return await conn.fetch(
        """SELECT id, text, descriptions
                    FROM game_question
                    WHERE category_id = $1 AND difficulty = 1
                    LIMIT 2
                    """,
        category,
    )


@psycopg2_cursor(DATABASE)
async def seclect_options_question(conn, q_id: int):
    return await conn.fetch(
        """SELECT id, text, true_answer
                        FROM game_questionoptions
                        WHERE question_id = $1
                        """,
        q_id,
    )


"""Функции с интерактивом"""


@psycopg2_cursor(DATABASE)
async def select_game_question(conn, user_id: int):
    """Получение вопросов интерактива."""
    result = await conn.fetch(
        """SELECT id, text, picture, cash, descriptions
                    FROM game_question
                    WHERE id NOT IN (
                        SELECT game_questionoptions.question_id
                        FROM game_answer
                        JOIN game_questionoptions ON game_answer.option_id = game_questionoptions.id
                        WHERE member_id = $1
                        ) AND is_active = true
                    """,
        user_id,
    )
    if not result:
        return None
    question = random.choice(result)
    options = await conn.fetch(
        """SELECT id, text, true_answer
                        FROM game_questionoptions
                        WHERE question_id = $1
                        """,
        question[0],
    )
    return question, options


@psycopg2_cursor(DATABASE)
async def insert_game_answer(cursor, user_id: int, option_id: int):
    """Добавление новых ответов пользователя."""
    await cursor.execute(
        """INSERT INTO game_answer(member_id, option_id, date) VALUES ($1,$2,$3)""",
        user_id,
        option_id,
        datetime.now(),
    )


@psycopg2_cursor(DATABASE)
async def delete_bag_question(connection, question_id: int):
    """Удалить вопрос, который не может отправить телеграм."""
    await connection.execute(
        """DELETE FROM game_questionoptions WHERE question_id=$1""",
        question_id,
    )
    await connection.execute(
        """DELETE FROM game_question WHERE id=$1""",
        question_id,
    )


@psycopg2_cursor(DATABASE)
async def insert_cash_photoquestion(conn, question_id: int, cash: str):
    """Добавить кэш-Id фотографии ранее присланной в боте к вопросу."""
    await conn.execute(
        """UPDATE game_question SET cash = $1 WHERE id = $2""", cash, question_id
    )


@psycopg2_cursor(DATABASE)
async def get_pin_message(conn):
    """Получить закрепленное сообщение."""
    return await conn.fetch(
        """SELECT text FROM call_support_pinmessage
        """
    )


@psycopg2_cursor(DATABASE)
async def insert_cash_photo(conn, letter_id: int, cash: str):
    """Добавить кэш-Id фотографии ранее присланной в боте к рассылке."""
    await conn.execute(
        """UPDATE call_support_newsletter SET cash = $1 WHERE id = $2""",
        cash,
        letter_id,
    )
