import os, json
import asyncio
import logging

from contextlib import suppress
from random import randint
from typing import Optional

from aiogram import Bot, Dispatcher, types, html, F
from aiogram.dispatcher.filters import CommandObject, Text
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hide_link
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.strategy import FSMStrategy

from aiogram import Router

#from config_reader import config
from handlers import start_les, groups, indiv, pie, participants, marking

#import func
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # Объект бота
    bot = Bot(token=os.getenv('tmTOKEN'), parse_mode="HTML")
    # Диспетчер
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_les.router)
    dp.include_router(groups.router)
    # dp.include_router(participants.router)
    # dp.include_router(marking.router)
    #

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
