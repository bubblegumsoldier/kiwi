import os
from logging import getLogger

AUTH_HEADER = 'Client-ID {}'

RATELIMIT_HEADER = "X-RateLimit-ClientRemaining"


class Requester:
    def __init__(self, session, template, extraction_function, start_page=1):
        self._template = template
        self._extraction_function = extraction_function
        self._page = start_page
        self._session = session

    async def request(self):
        url, headers = self._build_request()
        async with self._session.get(url, headers=headers) as response:
            self._page += 1
            self._check_rate_limit(response)
            json = await response.json()
            return await self._extraction_function(json['data'])

    def _build_request(self):
        url_template, tag, sort, window, secret, *_ = self._template
        url = url_template.format(tag=tag,
                                  sort=sort,
                                  window=window,
                                  page=self._page)
        headers = {'Authorization': AUTH_HEADER.format(secret)}
        getLogger("root").info("Requesting %s", url)
        return (url, headers)

    def _check_rate_limit(self, response):
        if (RATELIMIT_HEADER in response.headers
                and int(response.headers[RATELIMIT_HEADER]) < 1000):
            getLogger("root").warning("Remainging Rate Limit %d",
                                      response.headers[RATELIMIT_HEADER])

    @property
    def page(self):
        return self._page
