import os

import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType
from aiogram.utils import executor

from application.telegram_bot.bot_dto import BotAnswer
from application.telegram_bot.bot_processor import process_private_chat_message, process_public_chat_message, \
    process_start_command, process_new_jokes, process_stats_command

__bot_token = os.environ.get('API_TOKEN')
__update_jokes_token = os.environ.get('UPDATE_JOKES_TOKEN')

__bot = Bot(token=__bot_token)
dp = Dispatcher(__bot)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('serega')


@dp.message_handler(CommandStart())
async def start_command(msg: types.Message):
    await reply(msg=msg, answer=await process_start_command(msg))


@dp.message_handler(commands=['stats'])
async def stats_command(msg: types.Message):
    await reply(msg=msg, answer=await process_stats_command(msg=msg))


@dp.message_handler(commands=['add_new_jokes'], commands_ignore_caption=False, content_types=ContentType.DOCUMENT)
async def add_new_jokes(msg: types.Message):
    await reply(msg=msg, answer=await process_new_jokes(msg=msg, bot=__bot))


@dp.message_handler(lambda msg: msg.chat.type == "private")
async def private_chat_message(msg: types.Message):
    await reply(msg=msg, answer=await process_private_chat_message(msg))


@dp.message_handler(lambda msg: msg.chat.type != "private")
async def public_chat_message(msg: types.Message):
    await reply(msg=msg, answer=await process_public_chat_message(msg))


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    logger.exception("Cause exception {e} in update {update}", exception, update)
    return True


async def reply(msg: types.Message, answer: BotAnswer):
    if answer.is_reply:
        await msg.reply(answer.reply_text)
    if answer.is_joke:
        await __bot.send_message(chat_id=msg.chat.id, text=answer.joke_text)


def run_bot():
    logger.info("======================================\n" +
                "                              Bot-Sergey\n" +
                "================================================================================")
    executor.start_polling(dp)
