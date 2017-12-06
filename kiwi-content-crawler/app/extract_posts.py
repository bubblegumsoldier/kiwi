from functools import reduce
from data_access_functions import (get_many, post_exists)


def extract_posts_from_gallery(gallery_response, forbidden_types):
    '''
    Extract all posts that are no albums from the API Response.
    '''
    return filter_unsupported_formats(filter(lambda x: x['is_album'] is False,
                                             gallery_response['items']), forbidden_types)


def filter_duplicates(posts, predicate=post_exists):
    docs = ((predicate(post['id']), post) for post in posts)
    return (x[1] for x in filter(lambda x: not x[0], docs))


def get_new_posts(post_ids):
    return get_many(post_ids)


def filter_unsupported_formats(posts, formats):
    return list(
        filter(lambda x: not matches_forbidden_mimetypes(x, formats),
               posts))


def matches_forbidden_mimetypes(post, types):
    if 'type' in post:
        return post['type'].startswith(tuple(types))
    return True  # No type is also forbidden.
