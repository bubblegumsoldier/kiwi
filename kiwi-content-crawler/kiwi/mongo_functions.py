import logging
from copy import deepcopy
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


CLIENT = MongoClient(host="localhost", port=27017)
DB = CLIENT.get_database(name="imgur_posts")
COLLECTION = DB.get_collection("posts")


def insert_posts(posts):
    COLLECTION.insert_many(deepcopy(posts))
    return posts


def get_post(post_id):
    document = COLLECTION.find_one({"_id": post_id})
    return document  # potentially none


def get_many(post_ids):
    docs = [get_post(post_id) for post_id in post_ids]
    return filter(lambda x: x is not None, docs)


def post_exists(post_id):
    return COLLECTION.find_one({"id": post_id}) is not None
