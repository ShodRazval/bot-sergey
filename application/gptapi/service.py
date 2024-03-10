from application.gptapi.gpt_client import ChatGptClient
from application.gptapi.gpt_context import Dictionary
from application.gptapi.gpt_utils import remove_system


class GptService:
    client = ChatGptClient()
    context = Dictionary()

    def get_answer(self, message, chat_id):
        entries = self.context.add_entry_user(chat_id, message)
        answer = self.client.get_response(entries)
        self.context.add_entry_gpt(chat_id, answer)
        print(answer)
        return remove_system(answer)

    def dark_gpt(self, chat_id):
        self.context.set_dark_context(chat_id)

    def clear_context(self, chat_id):
        self.context.clear(chat_id)