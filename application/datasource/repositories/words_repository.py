import os

from pymongo.collection import Collection

from application.datasource.entity.words_data import Words



init_joke_trigers = ['анек', 'fytr', 'anek', 'шутк', 'преко', 'прико', 'joke', 'джоук']
init_foul_lang_trigers = ['[xхh](?:.?.?)[yуu](?:.?.?)[йiyеe]','пизд','жоп','нах','пезд','бля[д|т]','гандон','гнид','говн','дроч','еба','ебн','ебы','епт','ёба','ёбн','ёбы','ёпт','залуп','конч','лох','мраз','муда','педик','пидор','пидр','пизд','поскуд','сать','сосать','сука','уебан','хер','хуё','хует','хуит','хуя','шалав','шлюх','пидар','чмо','говн','гомн','жоп','сран','соси','соса','понос','панос','гадос','пенис','дура','дуры','рухля','толст']
init_greet_trigers = ['ghbd', 'прив', 'хай', 'hi', 'hello', 'хэло']

__my_name = ['серж', 'серг', 'serg', 'сереж', 'серёж', 'серый', 'serj', 'serej']


class WordsRepository:
    __words_collection_name = os.environ.get('MONGO_JOKE_TRIGGERS_COLLECTION_NAME')
    # __foul_lang_collection_name = os.environ.get('MONGO_FOUL_LANGUAGE_COLLECTION_NAME')

    # dictionary collcetion fields names
    __grop_field = os.environ.get('GROUP_FIELD_NAME')
    __triggers_field = os.environ.get('TRIGGERS_FIELD_NAME')
    __jokes_grope = os.environ.get('JOKE_TRIGGER_GROPE')
    __greetings_grope = os.environ.get('GREETINGS_TRIGGER_GROPE')
    __foul_lang_grope = os.environ.get('FOUL_LANG_TRIGGER_GROPE')

    __trigger_words_collection: Collection[Words]
    # __foul_lang_collection: Collection[Words]

    def __init__(self, mongo_connection):
        self.__trigger_words_collection = mongo_connection[self.__words_collection_name]
        self.update_joke_triggers(init_joke_trigers)
        self.update_greetings_triggers(init_greet_trigers)
        self.update_foul_triggers(init_foul_lang_trigers)

        # self.__foul_lang_collection = mongo_connection[self.__foul_lang_collection_name]

    def get_greet_triggers(self) -> list:
        return self.__trigger_words_collection.find_one({self.__grop_field: self.__greetings_grope})[self.__greetings_grope]

    def get_foul_triggers(self) -> list:
        return self.__trigger_words_collection.find_one({self.__grop_field: self.__foul_lang_grope})[self.__foul_lang_grope]

    def get_joke_triggers(self) -> list:
        return self.__trigger_words_collection.find_one({self.__grop_field: self.__jokes_grope})[self.__jokes_grope]
        # triggers = self.__joke_trigger_collection.find()
        # return triggers[self.__foul_lang_collection_name]

    def update_joke_triggers(self, data: list):
        json_data = data_to_document(self.__jokes_grope, data)
        self.__trigger_words_collection.update_one(
            {self.__grop_field: self.__jokes_grope},
            json_data,
            upsert=True
        )

    def update_greetings_triggers(self, data: list):
        json_data = data_to_document(self.__greetings_grope, data)
        self.__trigger_words_collection.update_one(
            {self.__grop_field: self.__greetings_grope},
            json_data,
            upsert=True
        )

    def update_foul_triggers(self, data: list):
        json_data = data_to_document(self.__foul_lang_grope, data)
        self.__trigger_words_collection.update_one(
            {self.__grop_field: self.__foul_lang_grope},
            json_data,
            upsert=True
        )


def data_to_document(words_group: str, data: list):
    return {"$addToSet": {words_group: {"$each": data}}}