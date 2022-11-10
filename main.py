import os, json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, html
from aiogram.dispatcher.filters import CommandObject
from aiogram.utils.markdown import hide_link
from aiogram.dispatcher.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import bot
'''
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.getenv('tmTOKEN'), parse_mode="HTML")

# Диспетчер
dp = Dispatcher()


'''
# Запуск процесса поллинга новых апдейтов
async def main():
    #dp.message.register(cmd_new_user, commands=["new_user"])
    #await dp.start_polling(bot)
    bot.asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())