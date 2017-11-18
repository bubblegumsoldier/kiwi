from kiwi.mongo_functions import (get_many, post_exists)


def extract_posts_from_gallery(gallery_response):
    """
    Extract all posts that are no albums from the API Response.
    """
    return list(filter(lambda x: x["is_album"] is False,
                       gallery_response["items"]))


def filter_duplicates(posts, predicate=post_exists):
    docs = ((predicate(post["id"]), post) for post in posts)
    return (x[1] for x in filter(lambda x: not x[0], docs))


def get_new_posts(post_ids):
    return get_many(post_ids)
