import re


def get_reply_username(message):
    if message.reply_to_message is not None\
            and message.reply_to_message.from_user is not None:
        username = message.reply_to_message.from_user.username
        if username is None:
            username = message.reply_to_message.from_user.first_name
        return username
    return "default"


def is_valid_string(string):
    if not string:
        return False
    for char in string:
        if char.isalnum():
            return True
    return False


def delete_my_name(text, words):
    for word in words:
        text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)
    return text.replace('@', '').strip()


def remove_system(text):
    txt = remove_half_string_before_word(text, "DarkGPT:")
    txt = txt.replace("DarkGPT:", '')
    system = "Enter a *Question* to let DarkGPT answer to it." #Ask for another question just by typing it!
    return txt.replace(system, '').strip()


def remove_half_string_before_word(string, word):
    index = string.find(word)
    if index == -1:
        return string
    new_string = string[index:]
    return new_string