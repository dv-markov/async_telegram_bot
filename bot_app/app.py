import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import aiohttp

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
    await message.answer(f"""Добро пожаловать, {hbold(message.from_user.full_name)}!
Введите код подтверждения, полученный на сайте realworker.ru для завершения регистрации""")


async def submit_verification_code(code, user_name, tg_id):
    async with aiohttp.ClientSession() as session:
        request_data = {
            'code': code,
            'telegram_id': tg_id,
            'telegram_name': user_name,
            'tg-bot-token': local_settings.DJANGO_ACCESS_KEY
        }
        async with session.post(
                local_settings.VERIFY_CODE_URL,
                data=request_data,
        ) as response:
            return await response.json()


@dp.message()
async def echo_handler(message: types.Message) -> None:
    text = message.text
    if len(text) == 6 and text.isnumeric():
        user_name = message.from_user.full_name
        tg_id = message.from_user.id
        res = await submit_verification_code(str(text), user_name, tg_id)
        auth = res.get('authorized')
        status = res.get('status')

        if auth:
            msg = 'Код подтвержден! '
            await message.answer(''.join((msg, status)), reply_markup=keyboards.inline_kb)
        else:
            msg = ''
            await message.answer(''.join((msg, status)))

    else:
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
