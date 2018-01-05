import os
from logging import getLogger

AUTH_HEADER = {
    'Authorization': 'Client-ID {}'.format(os.environ.get('IMGUR_CLIENT_ID'))}

RATELIMIT_HEADER = "X-RateLimit-ClientRemaining"


class Requester:
    def __init__(self, session, url_template, path, extraction_function):
        self._path = path
        self._extraction_function = extraction_function
        self.url = url_template
        self._page = 1
        self._session = session

    async def request(self):
        tag, sort, window, *_ = self._path

        url = self.url.format(tag=tag,
                              sort=sort,
                              window=window,
                              page=self._page)
        async with self._session.get(url, headers=AUTH_HEADER) as response:
            self._page += 1
            if RATELIMIT_HEADER in response.headers and response.headers[RATELIMIT_HEADER] < 1000:
                getLogger("root").warn("Remainging Rate Limit %d",
                                       response.headers[RATELIMIT_HEADER])
            json = await response.json()
            return await self._extraction_function(json['data'])

    @property
    def page(self):
        return self._page
