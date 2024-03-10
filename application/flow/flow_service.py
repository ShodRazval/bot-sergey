from aiogram.types import Message

from application.telegram_bot.bot_dto import BotAnswer


class FlowService:
    __flow_dict = dict()
    __default_flow = {0, 1}

    def __init__(self, flow_dict: dict):
        self.__flow_dict = flow_dict

    def handle(self, msg: Message) -> BotAnswer:
        answer = BotAnswer()
        # TODO: get chat settings context
        for check in self.__default_flow:
            self.__flow_dict[check].handle(msg, answer)
            if answer.is_end_check(): break

        return answer

    def get_current_flow(self, msg: Message) -> BotAnswer:
        answer = BotAnswer()
        chat_id = msg.chat.id
        # TODO: get chat settings context
        text = "Настройки:\n"

        for setting in self.__default_flow:
            text = text + f'\t{self.__flow_dict[setting].order()} : {self.__flow_dict[setting].description()}\n'

        text = text + 'Поменять набор настроек командой -> /кто_нажмет_тот_обезьяна'
        answer.set_joke(text)
        return answer

