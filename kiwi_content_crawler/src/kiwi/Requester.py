import os
from functools import partial
from collections import namedtuple
import requests
from extract_posts import store_posts_and_return_new_ids

BASE_URL = "https://api.imgur.com/3/gallery/t/{tag}/{sort}/{window}/{page}"
AUTH_HEADER = {
    "Authorization": "Client-ID {}".format(os.environ.get('IMGUR_CLIENT_ID'))}

Params = namedtuple("Params", "tag sort window")


class Requester(object):
    def __init__(self, base_params, post_cache):
        self._continue = True
        self._base_params = base_params
        self._post_cache = post_cache

    def request(self, page):
        tag, sort, window, *_ = self._base_params

        while self._continue:
            url = BASE_URL.format(tag=tag,
                                  sort=sort,
                                  window=window,
                                  page=page)
            response = requests.get(url, headers=AUTH_HEADER)
            posts = list(store_posts_and_return_new_ids(
                response.json()["data"]))
            self._post_cache.append(posts)
            page += 1
            

    def cancel(self):
        self._continue = False

