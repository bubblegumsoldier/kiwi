from kiwi.mongo_functions import insert_posts_filter_duplicates, get_many


def extract_posts_from_gallery(gallery_response):
    """
    Extract all posts that are no albums from the API Response.
    """
    return list(filter(lambda x: x["is_album"] is False,
                       gallery_response["items"]))


def store_posts_and_return_new_ids(gallery_response):
    """
    Inserts all posts into the database and returns only non-duplicate entry
    ids. Ids correspond to database keys and to Imgur API ids.
    """

    extracted_posts = extract_posts_from_gallery(gallery_response)
    results = insert_posts_filter_duplicates(extracted_posts)
    return list(results)


def store_and_return_new_posts(gallery_response):
    new_ids = store_posts_and_return_new_ids(gallery_response)
    return get_new_posts(new_ids)


def get_new_posts(post_ids):
    return get_many(post_ids)
