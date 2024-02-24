import os
import random
from datetime import datetime

from aiogram import types, Bot

from application.dataset_api.parse_utils import parse_html_jokes
from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.users_stats_repository import UserStatsRepository
from application.datasource.repositories.words_repository import WordsRepository
from application.telegram_bot.bot_dto import BotAnswer
from application.telegram_bot.message_utils import get_user_id, get_user_first_name, get_word_form

__joke_repository: JokesRepository
__users_repository: UserStatsRepository
__words_repository: WordsRepository

joke_triggers = set()
greet_triggers = set()
foul_lang_triggers = set()
__my_name = ['серж', 'серг', 'serg', 'сереж', 'серёж', 'серый', 'serj', 'serej']

last_time_joke = datetime.now()

__update_jokes_token = os.environ.get('UPDATE_JOKES_TOKEN')

supported_file_extension = '.html'  # TODO: should be used in process_new_jokes()


def init_processor(jokes_repository,
                   users_repository,
                   words_repository):
    global __joke_repository, __users_repository, __words_repository
    __joke_repository = jokes_repository
    __users_repository = users_repository
    __words_repository = words_repository

    for joke in __words_repository.get_joke_triggers():
        joke_triggers.add(joke)
    for greed in __words_repository.get_greet_triggers():
        greet_triggers.add(greed)
    for foul in __words_repository.get_foul_triggers():
        foul_lang_triggers.add(foul)


async def process_public_chat_message(msg: types.Message) -> BotAnswer:
    bot_answer = BotAnswer()
    user_first_name = get_user_first_name(msg)

    if any(word in msg.text.lower() for word in __my_name):
        if any(word in msg.text.lower() for word in foul_lang_triggers):
            __users_repository.fuck_off_inc(get_user_id(msg))
            bot_answer.set_reply(f'Пошел нахуй, {user_first_name}!')
            return bot_answer
        if any(word in msg.text.lower() for word in greet_triggers):
            bot_answer.set_reply(f'Здарова, {user_first_name}!')
        if any(word in msg.text.lower() for word in joke_triggers):
            bot_answer.set_joke(await __joke_repository.get_random_joke())
    else:
        delta = last_time_joke - datetime.now()
        if delta.total_seconds() / 60 / 60 > 1 and random.randint(1, 10) > 5:
            bot_answer.set_joke(__joke_repository.get_random_joke())
    return bot_answer


async def process_private_chat_message(msg: types.Message) -> BotAnswer:
    bot_answer = BotAnswer()
    user_first_name = get_user_first_name(msg)

    if any(word in msg.text.lower() for word in foul_lang_triggers):
        __users_repository.fuck_off_inc(get_user_id(msg))
        bot_answer.set_reply(f'Пошел нахуй, {user_first_name}!')
        return bot_answer
    if any(word in msg.text.lower() for word in greet_triggers):
        bot_answer.set_reply(f'Здарова, {user_first_name}!')
    if any(word in msg.text.lower() for word in joke_triggers):
        bot_answer.set_joke(__joke_repository.get_random_joke())
    return bot_answer


async def process_start_command(msg: types.Message) -> BotAnswer:
    bot_answer = BotAnswer()
    user_name = get_user_first_name(msg)
    user_id = get_user_id(msg)

    __users_repository.fuck_off_inc(user_id)
    bot_answer.set_reply(f'Отъебись, {user_name}!')
    return bot_answer


async def process_stats_command(msg: types.Message) -> BotAnswer:
    bot_answer = BotAnswer()
    user_name = get_user_first_name(msg)
    user_id = get_user_id(msg)

    fuck_off_count = __users_repository.find_user(user_id)
    bot_answer.set_reply(f'{user_name}, сходило нахуй {fuck_off_count} {get_word_form(fuck_off_count)}!')
    if random.randint(1, 10) == 1:
        bot_answer.set_joke(f'\"сходило\" потому что гендерно нейтрально')
    return bot_answer


async def process_new_jokes(msg: types.Message, bot: Bot) -> BotAnswer:
    bot_answer = BotAnswer()

    message_text = _get_message_text(msg)
    if not verify_token(message_text, __update_jokes_token):
        bot_answer.set_reply("Твой батя пидор, сынок")
    else:
        if is_supported_file_extension(msg.document.file_name):
            file = await bot.download_file_by_id(file_id=msg.document.file_id)
            jokes = parse_html_jokes(file)
            unprocessed_count = __joke_repository.insert_jokes_dataset(jokes)
            bot_answer.set_reply(f'Не получилось добавить {unprocessed_count} из {len(jokes)}')

    return bot_answer


def _get_message_text(message: types.Message) -> str:
    if message.text is not None:
        return message.text
    if message.html_text is not None:
        return message.html_text
    if message.md_text is not None:
        return message.md_text
    return ""


def verify_token(text: str, token: str) -> bool:
    if text.find(token) != -1:
        return True
    return False


def is_supported_file_extension(file_name: str) -> bool:
    extension = os.path.splitext(file_name)[1]
    if file_name.find(extension):
        return True
    return False
