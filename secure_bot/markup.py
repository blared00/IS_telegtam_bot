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

"""Кнопка Конечно"""
INLINE_KB_FACT = InlineKeyboardMarkup().row(
    InlineKeyboardButton("Конечно", callback_data="ofcourse_btn"),
    InlineKeyboardButton("Начать с азов", callback_data="back_main_btn")
)

def kb_onwards_link(link: str):
    """Кнопка далее."""
    return InlineKeyboardMarkup(row_width=1).insert(
        InlineKeyboardButton('Ссылка', url=link)).insert(
        InlineKeyboardButton("Далее", callback_data="onward_btn"))


"""Главное меню."""
INLINE_KB_MAIN = InlineKeyboardMarkup()
MAIN_KB = (
    ("Пройти тестирование", "main_game"),
    ("Обучение", "main_study"),
    ("Уровень компетентности", "main_level"),
)
filling_buttons(INLINE_KB_MAIN, MAIN_KB)

"""Выбор темы"""
INLINE_KB_MAIN_TEST = InlineKeyboardMarkup()
MAIN_TEST_KB = (
    ("Мобильные телефоны", "mobail_test"),
    ("Конфиденциальность", "conf_test"),
    ("Мессенджеры", "mess_test"),
    ("Пароли", "pass_test"),
    ("Системы", "sistem_test"),
    ("Электронная почта", "email_test"),
)
filling_buttons(INLINE_KB_MAIN_TEST, MAIN_TEST_KB)

"""Возврат в главное меню."""
INLINE_KB_BACKMENU = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Вернуться в главное меню", callback_data="back_main_btn")
)

"""Продолжить играть."""
INLINE_KB_BACKGAME = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton(random.choice(liters.ONWORDS_GAME).capitalize(), callback_data="mobail_test")).insert(
    InlineKeyboardButton("Вернуться в главное меню", callback_data="back_main_btn"))

"""Продолжить играть."""
INLINE_KB_LESSON = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton('Урок №1', callback_data="lesson_1")).insert(
    InlineKeyboardButton("Урок №2", callback_data="lesson_2")).insert(
    InlineKeyboardButton("Урок №3", callback_data="lesson_3"))

"""Вперед назад"""
INLINE_KB_RIGHT = InlineKeyboardMarkup().insert(
    InlineKeyboardButton('<Назад', callback_data="back")).insert(
    InlineKeyboardButton("Вперед>", callback_data="go"))