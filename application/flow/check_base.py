from abc import abstractmethod, ABCMeta

from aiogram.types import Message

from application.telegram_bot.bot_dto import BotAnswer


class CheckBase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, msg: Message, answer: BotAnswer) -> str:
        """Handle message, and return answer"""

    @abstractmethod
    def order(self) -> int:
        """Return order in flow"""

    @abstractmethod
    def description(self) -> str:
        """Return check description"""
