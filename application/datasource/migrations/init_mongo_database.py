import os
from pymongo.database import Database
from pymongo import MongoClient

__database_name = os.environ.get('MONGO_DATABASE_NAME')
__username = os.environ.get('MONGO_DB_USERNAME')
__password = os.environ.get('MONGO_DB_PASSWORD')
__host = os.environ.get('MONGO_HOST')
__port = os.environ.get('MONGO_PORT')

__users_collection_name = os.environ.get('MONGO_USERS_COLLECTION_NAME')
__jokes_collection_name = os.environ.get('MONGO_JOKES_COLLECTION_NAME')
__words_collection_name = os.environ.get('MONGO_JOKE_TRIGGERS_COLLECTION_NAME')

# jokes collection fields names
__hash_field = os.environ.get('JOKES_HASH_FIELD_NAME')
__text_field = os.environ.get('JOKES_TEXT_FIELD_NAME')
__hash_index = os.environ.get('JOKES_HASH_INDEX_NAME')

# users stats collection fields names
__user_id_field = os.environ.get('USER_ID_FIELD_NAME')
__stats_field = os.environ.get('USER_STATS_FIELD_NAME')
__user_index = os.environ.get('USER_INDEX_NAME')

# dictionary collection fields names
__grop_field = os.environ.get('GROUP_FIELD_NAME')
__triggers_field = os.environ.get('TRIGGERS_FIELD_NAME')
__jokes_grope = os.environ.get('JOKE_TRIGGER_GROPE')
__greetings_grope = os.environ.get('GREETINGS_TRIGGER_GROPE')

__data_base_connection: Database
__mongo_client: MongoClient


def init_db():
    mongo_client = MongoClient(host=__host,
                               port=int(__port),
                               username=__username,
                               password=__password,
                               authMechanism='SCRAM-SHA-256')

    bot_serega_db_connection: Database

    if __database_name not in mongo_client.list_database_names():
        print(f'Warn! DataBase <{__database_name}> does not exist!')
        bot_serega_db_connection = mongo_client[__database_name]
    else:
        bot_serega_db_connection = mongo_client.get_database(__database_name)

    users_collection = bot_serega_db_connection[__users_collection_name]
    jokes_collection = bot_serega_db_connection[__jokes_collection_name]
    words_collection = bot_serega_db_connection[__words_collection_name]

    users_collection.create_index([(__user_id_field, 1)], name=__user_index, unique=True)
    jokes_collection.create_index([(__hash_field, 1)], name=__hash_index, unique=True)

    global __data_base_connection, __mongo_client
    __mongo_client = mongo_client
    __data_base_connection = bot_serega_db_connection


def get_mongo_connection():
    global __data_base_connection
    return __data_base_connection


def get_mongo_client():
    global __mongo_client
    return __mongo_client

