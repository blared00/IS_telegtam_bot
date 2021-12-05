from aiogram import types

import liters
import markup
from create_bot import dp
from utils import BotState


@dp.callback_query_handler(lambda c: c.data == 'main_study',
                           state=BotState.MAIN)
async def education_main(callback_query: types.CallbackQuery):
    """Возвращает в меню обучения с выбором тем.
         _____
        Кнопки:
        Срабатывание - 'Обучение',
        Создает - темы."""
    await callback_query.answer()
    await callback_query.message.edit_text(
        liters.MAIN_TEST_MENU,
        reply_markup=markup.INLINE_KB_MAIN_TEST
    )
    await BotState.NEWLESSON.set()


@dp.callback_query_handler(lambda c: c.data in [kb[1] for kb in markup.MAIN_TEST_KB],
                           state=BotState.NEWLESSON)
async def choose_lesson(callback_query: types.CallbackQuery):
    """Возвращает в меню обучения с выбором тем.
     _____
    Кнопки:
    Срабатывание - одна из выбранных тем
    Создает - уроки."""
    await callback_query.answer()
    await callback_query.message.edit_text(
        liters.MAIN_EDU_MENU,
        reply_markup=markup.INLINE_KB_LESSON
    )

@dp.callback_query_handler(lambda c: c.data in ['lesson_1','lesson_2','lesson_3'],
                           state=BotState.NEWLESSON)
async def choose_lesson(callback_query: types.CallbackQuery):
    """Возвращает в меню обучения с выбором тем.
     _____
    Кнопки:
    Срабатывание - Один из уроков
    Создает - материалы урока"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        liters.EDU_L1,
        reply_markup=markup.INLINE_KB_RIGHT
    )


@dp.callback_query_handler(lambda c: c.data in ["go"],
                           state=BotState.NEWLESSON)
async def choose_lesson(callback_query: types.CallbackQuery):
    """Возвращает в меню обучения с выбором тем.
     _____
    Кнопки:
    Срабатывание - Один из уроков
    Создает - материалы урока"""
    await callback_query.answer()
    await callback_query.message.edit_text(
        liters.EDU_LINK,
        reply_markup=markup.INLINE_KB_BACKMENU
    )
