import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import aiohttp
import ssl
import certifi

import local_settings
import keyboards


TOKEN = local_settings.API_KEY

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"""Добро пожаловать, {hbold(message.from_user.full_name)}!
Вас приветствует телеграм-бот сайта realworker.ru 
Для завершения регистрации подтвердите свой телефон нажатием кнопки "Отправить контакт" ниже""",
        reply_markup=keyboards.contact_kb,
    )


# async def submit_verification_code(code, user_name, tg_id):
#     ssl_context = ssl.create_default_context(cafile=certifi.where())
#     async with aiohttp.ClientSession() as session:
#         request_data = {
#             'code': code,
#             'telegram_id': tg_id,
#             'telegram_name': user_name,
#             'tg-bot-token': local_settings.DJANGO_ACCESS_KEY
#         }
#         async with session.post(
#                 local_settings.VERIFY_CODE_URL,
#                 data=request_data,
#                 ssl=ssl_context,
#         ) as response:
#             return await response.json()


async def submit_phone(phone, user_name, tg_id):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession() as session:
        request_data = {
            'phone': phone,
            'tg_id': tg_id,
            'tg_name': user_name,
            'tg_bot_token': local_settings.DJANGO_ACCESS_KEY
        }
        async with session.patch(
                local_settings.VERIFY_PHONE_URL,
                data=request_data,
                ssl=ssl_context,
        ) as response:
            return await response.json(content_type='application/json')


@dp.message(F.contact)
async def contact_handler(message: types.Message) -> None:
    verified = None
    try:
        phone = message.contact.phone_number
        user_name = message.from_user.full_name
        tg_id = message.from_user.id
        res = await submit_phone(phone, user_name, tg_id)
        verified = res.get('verified')
    except Exception as e:
        msg = f"Ошибка верификации, {e}"
        await message.answer(msg)

    if verified:
        msg = 'Телефон подтвержден!'
        await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    else:
        msg = 'Телефон не подтвержден, пройдите регистрацию на сайте realworker.ru'
        await message.answer(msg)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    # text = message.text
    # if len(text) == 6 and text.isnumeric():
    #     user_name = message.from_user.full_name
    #     tg_id = message.from_user.id
    #     res = await submit_verification_code(str(text), user_name, tg_id)
    #     auth = res.get('authorized')
    #     status = res.get('status')
    #
    #     if auth:
    #         msg = 'Код подтвержден! '
    #         await message.answer(''.join((msg, status)), reply_markup=keyboards.inline_kb_site)
    #     else:
    #         msg = ''
    #         await message.answer(''.join((msg, status)))
    #
    # if len(text) == 11 and text.isnumeric():
    #     user_name = message.from_user.full_name
    #     tg_id = message.from_user.id
    #     res = await submit_phone(str(text), user_name, tg_id)
    #     print(res)
    #     verified = res.get('verified')
    #
    #     if verified:
    #         msg = 'Телефон подтвержден!'
    #         await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    #     else:
    #         msg = 'Телефон не подтвержден, пройдите регистрацию на сайте'
    #         await message.answer(msg, reply_markup=keyboards.inline_kb_site)
    # else:
    try:
        await message.reply("Команда не найдена")
    except TypeError:
        await message.reply("Неподдерживаемый тип данных")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
