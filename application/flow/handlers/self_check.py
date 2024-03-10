from aiogram.types import Message

from application.flow.check_base import CheckBase
from application.telegram_bot.bot_dto import BotAnswer


class SelfCheck(CheckBase):
    __order = 0
    __description = "Реагировать только если упонимается имя бота"

    __my_name = ['sergey_trudovichkov_bot', 'серж', 'серг', 'сереж', 'серёж', 'серёг', 'серый', 'serg', 'serj', 'serej']

    __self_triggers = set()

    def __init__(self):
        for name in self.__my_name:
            self.__self_triggers.add(name)

    def handle(self, msg: Message, answer: BotAnswer):
        if any(word in msg.text.lower() for word in self.__self_triggers):
            pass
        else:
            answer.end_flow()

    def order(self) -> int:
        return self.__order

    def description(self) -> str:
        return self.__description
