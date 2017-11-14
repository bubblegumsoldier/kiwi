import logging
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
CLIENT = MongoClient(host="localhost", port=27017)
DB = CLIENT.get_database(name="imgur_posts")
COLLECTION = DB.get_collection("posts")


def insert_post(post):
    try:
        response = COLLECTION.insert_one(update_post_with_id(post))
        return response.inserted_id, response.acknowledged
    except DuplicateKeyError:
        logging.warning("Duplicate key.")
        return None, False


def insert_posts_filter_duplicates(posts):
    results = [insert_post(post)[0] for post in posts]
    return filter(lambda x: x is not None, results)


def id_exists(post):
    post_id = post["id"]
    cursor = COLLECTION.find({"_id": post_id})
    return cursor.count > 0


def update_post_with_id(post):
    id_dict = {"_id": post["id"]}
    id_dict.update(post)
    return id_dict


def get_post(post_id):
    document = COLLECTION.find_one({"_id": post_id})
    return document  # potentially none


def get_many(post_ids):
    docs = [get_post(post_id) for post_id in post_ids]
    return filter(lambda x: x is not None, docs)
