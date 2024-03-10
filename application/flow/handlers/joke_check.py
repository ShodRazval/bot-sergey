from aiogram.types import Message

from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.words_repository import WordsRepository
from application.flow.check_base import CheckBase
from application.telegram_bot.bot_dto import BotAnswer


class JokeCheck(CheckBase):
    __order = 1
    __description = "Проверяет наличие тригера на анекдот"

    __joke_repository: JokesRepository

    joke_triggers = set()

    def __init__(self, jokes_repository: JokesRepository, words_repository: WordsRepository):
        self.__joke_repository = jokes_repository
        for joke in words_repository.get_joke_triggers():
            self.joke_triggers.add(joke)

    def handle(self, msg: Message, answer: BotAnswer):
        if any(word in msg.text.lower() for word in self.joke_triggers):
            answer.set_joke(self.__joke_repository.get_random_joke())

    def order(self) -> int:
        return self.__order

    def description(self) -> str:
        return self.__description
