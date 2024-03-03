class User:
    user_id: int
    user_first_name: str
    user_fuck_of_count: int

    def __init__(self, user_id: int, user_first_name: str, user_fuck_of_count: int):
        self.user_id = user_id
        self.user_first_name = user_first_name
        self.user_fuck_of_count = user_fuck_of_count


class ChatStatistic:
    chat_id: int
    users: list

    def add_user(self, user_id: int, user_first_name: str):
        user = self.users.find(lambda x: x.user_id == user_id)
        if user is None:
            new_user = User(user_id, user_first_name, 0)
            self.users.append(new_user)

