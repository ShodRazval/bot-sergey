import os

import logging
import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType
from aiogram.utils import executor


from application.dataset_api.parse_utils import ParseUtils
from application.datasource.repositories.users_stats_repository import UserStatsRepository
from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.words_repository import WordsRepository

from application.telegram_bot.message_utils import get_user_first_name, get_user_id, get_word_form


from datetime import datetime

__bot_token = users = os.environ.get('API_TOKEN')
__update_jokes_token = os.environ.get('UPDATE_JOKES_TOKEN')


__bot = Bot(token=__bot_token)
dp = Dispatcher(__bot)
__joke_repository: JokesRepository
__users_repository: UserStatsRepository
__words_repository: WordsRepository
__parse_utils: ParseUtils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('serega')

joke_trigers = set()
greet_trigers = set()
foul_lang_trigers = set()
    # = ['анек', 'fytr', 'anek', 'шутк', 'преко', 'прико', 'joke', 'джоук']


__my_name = ['серж', 'серг', 'serg', 'сереж', 'серёж', 'серый', 'serj', 'serej']


last_time_joke = datetime.now()

# Инициализация клиента для запросов к ChatGPT
# __gpt_service = GptService()


def init_bot_handlers(jokes_repository,
                      users_repository,
                      words_repository,
                      parse_utils):
    global __joke_repository, __users_repository, __words_repository, __parse_utils
    __joke_repository = jokes_repository
    __users_repository = users_repository
    __words_repository = words_repository
    __parse_utils = parse_utils

    for joke in __words_repository.get_joke_triggers():
        joke_trigers.add(joke)
    for greed in __words_repository.get_greet_triggers():
        greet_trigers.add(greed)
    for foul in __words_repository.get_foul_triggers():
        foul_lang_trigers.add(foul)

    # joke_trigers.add(__words_repository.get_joke_triggers())
    # greet_trigers.add(__words_repository.get_greet_triggers())
    # foul_lang_trigers.add(__words_repository.get_foul_triggers())

# GPT =========================================================================

# @dp.message_handler(commands=['clear_context'])
# async def start_cmd_handler(message: types.Message):
#     __gpt_service.clear_context(chat_id=message.chat.id)
#     await message.answer(
#         "Все, забыли"
#     )
#
# # Обработка всех сообщений кроме команд где упоминается имя бота
# @dp.message_handler(
#     lambda msg: any(word in msg.text.lower() for word in __my_name) and msg.chat.type != "private"
# )
# async def echo_message(msg: types.Message):
#     txt = delete_my_name(msg.text, __my_name)
#     # print(msg)
#     if is_valid_string(txt):
#         response = __gpt_service.get_answer(txt, chat_id=msg.chat.id)
#         await __bot.send_message(chat_id=msg.chat.id, text=response)
#
# @dp.message_handler(
#     lambda msg: msg.chat.type == "private"
# )
# async def echo_message(msg: types.Message):
#     # print(msg)
#     # if is_valid_string(msg):
#     response = __gpt_service.get_answer(msg.text, chat_id=msg.chat.id)
#     await __bot.send_message(chat_id=msg.chat.id, text=response)

# GPT =========================================================================




# @dp.message_handler(lambda msg: msg.text.lower() in joke_trigers)

@dp.message_handler(
    lambda msg: msg.chat.type == "private"
)
async def echo_message(msg: types.Message):
    # delta = last_time_joke - datetime.now()
    if any(word in msg.text.lower() for word in foul_lang_trigers) :
        __users_repository.fuck_off_inc(get_user_id(msg))
        await msg.reply(f'Пошел нахуй, {get_user_first_name(msg)}!')
        return
    if any(word in msg.text.lower() for word in greet_trigers) :
        await msg.reply(f'Здарова, {get_user_first_name(msg)}!')
    if any(word in msg.text.lower() for word in joke_trigers) :
        await __bot.send_message(chat_id=msg.chat.id, text=__joke_repository.get_random_joke())

# @dp.message_handler(
#     lambda msg: msg.chat.type != "private"
# )
@dp.message_handler(
    lambda msg: any(word in msg.text.lower() for word in __my_name) and msg.chat.type != "private"
)
async def message_handler(msg: types.Message):
    if any(word in msg.text.lower() for word in foul_lang_trigers) :
        __users_repository.fuck_off_inc(get_user_id(msg))
        await msg.reply(f'Пошел нахуй, {get_user_first_name(msg)}!')
        return
    if any(word in msg.text.lower() for word in greet_trigers) :
        await msg.reply(f'Здарова, {get_user_first_name(msg)}!')
    if any(word in msg.text.lower() for word in joke_trigers) :
        await __bot.send_message(chat_id=msg.chat.id, text=__joke_repository.get_random_joke())
    # joke = __joke_repository.get_random_joke()
    # await message.answer(joke)

#
# @dp.message_handler(
#     lambda msg: msg.chat.type != "private"
# )
# async def message_handler(msg: types.Message):
#     delta = last_time_joke - datetime.now()
#     if delta.total_seconds()/60/60 > 1 and random.randint(1, 27) > 5:
#         await __bot.send_message(chat_id=msg.chat.id, text=__joke_repository.get_random_joke())
    # joke = __joke_repository.get_random_joke()
    # await message.answer(joke)


@dp.message_handler(CommandStart())
async def message_handler(message: types.Message):
    user_name = get_user_first_name(message)
    user_id = get_user_id(message)
    #TODO: get foul language
    # foul_word = foul_lang_trigers.
    await __users_repository.fuck_off_inc(user_id)
    await message.reply(f'Пошел нахуй, {user_name}!')
    # await message.reply(f'{user_name} сходил нахуй {user_stats} {get_word_form(user_stats)}')

# @dp.message_handler(filters.Text(contains=['add_new_jokes'], ignore_case=True), content_types=ContentType.DOCUMENT)
@dp.message_handler(commands=['add_new_jokes'], commands_ignore_caption=False, content_types=ContentType.DOCUMENT)
async def add_new_jokes(message: types.Message):

    print(f'\n\n\n{message}\n\n\n')
    print(f'\n\n\n{message.document.file_id}\n\n\n')

    message_text = get_message_text(message)
    if not have_privilege(message_text, __update_jokes_token):
        await message.answer(invalid_token_message())
        return
    else:
        if is_supported_file_extension(message.document.file_name):
            file = await __bot.download_file_by_id(file_id=message.document.file_id)
            __parse_utils.parse_html_jokes(file)
            await message.answer('все путем')
            return
    await message.answer(invalid_token_message())
    return

# @dp.message_handler(commands=['add_greet_trig'], commands_ignore_caption=False, content_types=ContentType.DOCUMENT)
# async def add_new_greet(message: types.Message):
#
#     print(f'\n\n\n{message}\n\n\n')
#     print(f'\n\n\n{message.document.file_id}\n\n\n')
#
#     message_text = get_message_text(message)
#     if not have_privilege(message_text, __update_jokes_token):
#         await message.answer(invalid_token_message())
#         return
#     else:
#         if is_supported_file_extension(message.document.file_name):
#             file = await __bot.download_file_by_id(file_id=message.document.file_id)
#             __parse_utils.add_greetings_triggers(file.read().decode('utf-8'))
#             await message.answer('все путем')
#             return
#     await message.answer(invalid_token_message())
#     return
#
# @dp.message_handler(commands=['add_foul_trig'], commands_ignore_caption=False, content_types=ContentType.DOCUMENT)
# async def add_foul_lang(message: types.Message):
#
#     print(f'\n\n\n{message}\n\n\n')
#     print(f'\n\n\n{message.document.file_id}\n\n\n')
#
#     message_text = get_message_text(message)
#     if not have_privilege(message_text, __update_jokes_token):
#         await message.answer(invalid_token_message())
#         return
#     else:
#         if is_supported_file_extension(message.document.file_name):
#             file = await __bot.download_file_by_id(file_id=message.document.file_id)
#             __parse_utils.add(file.read().decode('utf-8'))
#             await message.answer('все путем')
#             return
#     await message.answer(invalid_token_message())
#     return


def is_supported_file_extension(file_name):
    extension = os.path.splitext(file_name)[1]
    if file_name.find(extension):
        return True
    return False

    # else:
        # file_id = message.document.file_id
        #
        # file = get_file(file_id).download()

        # await message.answer(answer)

    # answer: str
    # if not have_privilege(message.text, __update_jokes_token):
    #     answer = invalid_token_message()
    # else:

    # print("ABOBA работает?")
    # print(file)

    # global __update_joks_token
    # text = message.text
    # if __update_joks_token in text:


    #     await message.answer('Начинается обработка');
    #     file = get_file(message.document).download()
    #     await message.answer('Реестр успешно обработан!');
    #
    # print(message)
    # await message.answer("Привет")

    # await message.answer("есть пробитие")
    # file = get_file(message.document).download()
    # print(f'file = {file:>10}')
    # print(f'file name = {message.document.file_name:>10}')
    # with open("custom/file.doc", 'wb') as f:
    #     context.bot.get_file(update.message.document).download(out=f)

@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    logger.exception("Cause exception {e} in update {update}", e=exception, update=update)
        # sentry_sdk.capture_exception(e)
    return True


def invalid_token_message():
    return "Твой батя пидор, сынок..."

def run_bot():
    executor.start_polling(dp)

def have_privilege(text: str, token: str):
    if text.find(token) != -1:
        return True
    return False

def get_message_text(message: types.Message):
    if message.text is not None:
        return message.text
    if message.html_text is not None:
        return message.html_text
    if message.md_text is not None:
        return message.md_text
    return ""
