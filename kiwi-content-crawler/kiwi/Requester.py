import os
from collections import namedtuple
import requests
from extract_posts import extract_posts_from_gallery

BASE_URL = "https://api.imgur.com/3/gallery/t/{tag}/{sort}/{window}/{page}"
AUTH_HEADER = {
    "Authorization": "Client-ID {}".format(os.environ.get('IMGUR_CLIENT_ID'))}

Params = namedtuple("Params", "tag sort window")


class Requester(object):
    def __init__(self, base_params):
        self._continue = True
        self._base_params = base_params
        self._page = 1

    def request(self, continuation):
        tag, sort, window, *_ = self._base_params

        url = BASE_URL.format(tag=tag,
                              sort=sort,
                              window=window,
                              page=self._page)

        response = requests.get(url, headers=AUTH_HEADER)
        posts = extract_posts_from_gallery(
            response.json()["data"])
        self._page += 1
        return continuation(posts)
