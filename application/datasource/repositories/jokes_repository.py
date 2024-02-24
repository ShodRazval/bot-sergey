import hashlib
import os
import random

from pymongo.collection import Collection

from application.datasource.entity.joke_data import Joke


class JokesRepository:
    __jokes_collection_name = os.environ.get('MONGO_JOKES_COLLECTION_NAME')

    # jokes collection fields names
    __hash_field = os.environ.get('JOKES_HASH_FIELD_NAME')
    __text_field = os.environ.get('JOKES_TEXT_FIELD_NAME')
    __hash_index = os.environ.get('JOKES_HASH_INDEX_NAME')

    __default_joke_text = "Я забыл ВСЕ анекдоты..."

    __jokes_collection: Collection[Joke]

    def __init__(self, mongo_connector):
        self.__jokes_collection = mongo_connector[self.__jokes_collection_name]

    def get_random_joke(self) -> str:
        dock_count = self.__jokes_collection.count_documents({})
        if dock_count == 0:
            return self.__default_joke_text
        random_number = random.randint(0, dock_count)
        joke_text = self.__jokes_collection.find().limit(-1).skip(random_number).next()
        return joke_text[self.__text_field]

    def insert_jokes_dataset(self, jokes_list) -> int:
        unprocessed_count = 0
        for joke in jokes_list:
            try:
                joke_json = self.joke_to_json(joke)
                self.__jokes_collection.insert_one(joke_json)
            except Exception as ex:
                unprocessed_count += 1
                print(ex)
                print(joke)
        return unprocessed_count

    def joke_to_json(self, text: str):
        hash_id = calculate_hash(text)
        return {self.__hash_field: hash_id, self.__text_field: text}


def calculate_hash(text: str) -> str:
    return str(int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16))
