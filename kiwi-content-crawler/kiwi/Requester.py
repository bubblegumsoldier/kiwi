import os
import requests
from extract_posts import extract_posts_from_gallery


AUTH_HEADER = {
    'Authorization': 'Client-ID {}'.format(os.environ.get('IMGUR_CLIENT_ID'))}

class Requester:
    def __init__(self, url, params):
        self._continue = True
        self._params = params
        self.url = url
        self._page = 1

    def request(self, continuation):
        tag, sort, window, *_ = self._params

        url = self.url.format(tag=tag,
                              sort=sort,
                              window=window,
                              page=self._page)

        response = requests.get(url, headers=AUTH_HEADER)
        posts = extract_posts_from_gallery(
            response.json()['data'])
        self._page += 1
        return continuation(posts)
