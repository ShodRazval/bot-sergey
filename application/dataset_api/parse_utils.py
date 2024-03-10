from bs4 import BeautifulSoup

required_file_extension = '.html'

haram_words = {'Видео Долбоёба', 'ничё)', 'ачё)' 'Shot post', 'Cursed images', 'WEBM', 'подписчики', 'подпишитесь'}

def parse_html_jokes(file: str) -> list:
    soup = BeautifulSoup(file, 'html.parser')
    jokes = [tag.get_text(separator="\n") for tag in soup.findAll('div', {"class": "text"})]
    return beautify_jokes(jokes)


def beautify_jokes(jokes: list) -> list:
    global haram_words
    jokes_parsed = []
    for joke in jokes:
        if any(word in joke.lower() for word in haram_words):
            print(joke)
            print('\n=====================================================================================================================================\n')
        else:
            tmp = joke.strip()
            if len(tmp) > 10 and tmp.find('http') == -1:
                jokes_parsed.append(tmp)
    return jokes_parsed


def beautify_triggers(words: str) -> list:
    split_lines = words.split('\n')
    result = []
    for word in split_lines:
        tmp = word.strip()
        if tmp != "":
            result.append(tmp)
    return result


def read_file(file_name):
    f = open(file_name, 'r', encoding='UTF-8')
    file_data = f.read()
    f.close()
    return file_data
