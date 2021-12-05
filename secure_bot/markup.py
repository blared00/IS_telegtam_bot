import random

try:
    import liters
except ModuleNotFoundError:
    from secure_bot import liters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def filling_buttons(keyboard: InlineKeyboardMarkup, tuple_key: tuple):
    """Добавление кортежа Имени и Калбэк_данных в маркап."""
    for text, cbq in tuple_key:
        keyboard.row(InlineKeyboardButton(text, callback_data=cbq))


def range_inline_kb(number: int, postfix: str, options: list = [], row_size=5):
    """Создание кнопок для ответы на вопросы"""
    if options:
        keyboards = map(lambda x: InlineKeyboardButton(options[x-1], callback_data=str(x) + postfix), range(1, number + 1))
    else:
        keyboards = map(lambda x: InlineKeyboardButton(str(x), callback_data=str(x) + postfix), range(1, number + 1))
    key_markup = InlineKeyboardMarkup(row_width=row_size)
    for key in keyboards:
        key_markup.insert(key)
    return key_markup


INLINE_KB_WELCOME = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Привет, хочу начать обучение", callback_data="welcome_btn")
)

# """Участие в велком-встрече."""
# INLINE_KB_METING = InlineKeyboardMarkup()
# METING_KB = (("Да", "yes_meting_button"), ("Нет", "no_meting_button"))
# filling_buttons(INLINE_KB_METING, METING_KB)

"""Кнопка Конечно"""
INLINE_KB_FACT = InlineKeyboardMarkup().row(
    InlineKeyboardButton("Конечно", callback_data="ofcourse_btn"),
    InlineKeyboardButton("Начать с азов", callback_data="back_main_btn")
)

# """Кнопка ценности."""
# INLINE_KB_WORTH = InlineKeyboardMarkup().row(
#     InlineKeyboardButton("А ценности?", callback_data="worth_btn")
# )


def kb_onwards_link(link: str):
    """Кнопка далее."""
    return InlineKeyboardMarkup(row_width=1).insert(
        InlineKeyboardButton('Ссылка', url=link)).insert(
        InlineKeyboardButton("Далее", callback_data="onward_btn"))


"""Как долго работает."""
INLINE_KB_HOW_LONG = InlineKeyboardMarkup()
HOW_LONG_KB = (
    ("Менее двух недель", "less_2"),
    ("2 - 6 недель", "2_6_week"),
    ("6 - 12 недель", "6_12_week"),
    ("Более 12 недель", "more_12"),
)
filling_buttons(INLINE_KB_HOW_LONG, HOW_LONG_KB)
#ХУЙ
"""Главное меню."""
INLINE_KB_MAIN = InlineKeyboardMarkup()
MAIN_KB = (
    ("Поиграем?", "main_game"),
    ("Обучение", "main_study"),
)
filling_buttons(INLINE_KB_MAIN, MAIN_KB)

"""Возврат в главное меню."""
INLINE_KB_BACKMENU = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Вернуться в главное меню", callback_data="back_main_btn")
)

"""Продолжить играть."""
INLINE_KB_BACKGAME = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton(random.choice(liters.ONWORDS_GAME).capitalize(), callback_data="main_game")).insert(
    InlineKeyboardButton("Вернуться в главное меню", callback_data="back_main_btn"))

"""Меню помощи."""
INLINE_KB_HELP_MENU = InlineKeyboardMarkup()
HELP_KB = (
    ("Вопросы по з/п", "help_pay"),
    ("Вопросы по порталу", "help_web"),
    ("Вопросы по документам", "help_doc"),
    ("Контакты департамента по работе с персоналом", "help_hr_contact"),
    ("Помощники чат-бота Марты", "help_bot_contact"),
    ("Задать свой вопрос", "help_ask"),
    ("Ваши вопросы", "help_question"),
    ("Вернуться в главное меню", "back_main_btn"),
)
filling_buttons(INLINE_KB_HELP_MENU, HELP_KB)

"""Вопросы по порталу."""
INLINE_KB_HELP_WEB = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton("Ссылка для входа на портал", url="https://portal.mrtexpert.ru/")).insert(
    InlineKeyboardButton("Вернуться в меню помощи", callback_data="back_help_btn"))

"""Вопросы по документам."""
INLINE_KB_HELP_DOC = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton("Ссылка для входа в раздел", url="https://portal.mrtexpert.ru/folders")).insert(
    InlineKeyboardButton("Вернуться в меню помощи", callback_data="back_help_btn"))

"""Вернуться в меню помощи"""
INLINE_KB_BACKHELP = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Вернуться в меню помощи", callback_data="back_help_btn"))

"""Задать вопрос или вернуться в главное меню"""
INLINE_KB_ASK_Q = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton("Задать вопрос оператору", callback_data="ask")).insert(
    InlineKeyboardButton("Вернуться в главное меню", callback_data="back_main_btn"))
