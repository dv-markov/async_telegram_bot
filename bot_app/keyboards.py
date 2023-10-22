from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# inline_button_site = InlineKeyboardButton(text="Перейти на сайт",
#                                           url='https://realworker.ru',
#                                           )
# inline_kb_site = InlineKeyboardMarkup(inline_keyboard=[[inline_button_site]])
# inline_kb.add(inline_button_site)

contact_button = KeyboardButton(text='Отправить контакт',
                                request_contact=True,
                                )
contact_kb = ReplyKeyboardMarkup(keyboard=[[contact_button]],
                                 resize_keyboard=True,
                                 # one_time_keyboard=True,
                                 )


