from copy import deepcopy
from pymongo import MongoClient
from kiwi.config import read_mongo_config


CONFIG = read_mongo_config()
CLIENT = MongoClient(host=CONFIG.host, port=CONFIG.port, authSource=CONFIG.db,
                     username=CONFIG.username, password=CONFIG.password)


def _get_collection():
    return CLIENT[CONFIG.db][CONFIG.collection]


def insert_posts(posts):
    _get_collection().insert_many(deepcopy(posts))
    return posts


def get_post(post_id):
    document = _get_collection().find_one({'_id': post_id})
    return document  # potentially none


def get_many(post_ids):
    docs = [get_post(post_id) for post_id in post_ids]
    return filter(lambda x: x is not None, docs)


def post_exists(post_id):
    return _get_collection().find_one({'id': post_id}) is not None
