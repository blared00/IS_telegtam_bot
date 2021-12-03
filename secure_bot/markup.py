from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


INLINE_KB_WELCOME = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Привет!", callback_data="welcome_btn")
)
