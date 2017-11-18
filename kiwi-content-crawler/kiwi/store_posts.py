from kiwi.mongo_functions import insert_posts


def store_posts_continuation(continuation, posts):
    insert_posts(posts)
    continuation(posts)
