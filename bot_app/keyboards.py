from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

inline_button_site = InlineKeyboardButton(text="Перейти на сайт", url='https://realworker.ru')
inline_kb = InlineKeyboardMarkup(inline_keyboard=[[inline_button_site]])
# inline_kb.add(inline_button_site)

