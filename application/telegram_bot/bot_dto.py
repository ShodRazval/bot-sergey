class BotAnswer:
    is_end: bool

    is_reply: bool
    is_joke: bool
    reply_text: str
    joke_text: str

    def __init__(self):
        self.is_reply = False
        self.is_joke = False
        self.is_end = False

    def set_reply(self, reply_text):
        self.is_reply = True
        self.reply_text = reply_text

    def set_joke(self, reply_text):
        self.is_joke = True
        self.joke_text = reply_text

    def end_flow(self):
        self.is_end = True

    def is_end_check(self) -> bool:
        return self.is_end
