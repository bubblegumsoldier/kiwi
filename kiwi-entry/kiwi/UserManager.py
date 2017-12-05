from aiohttp.client import ClientSession
from http import HTTPStatus
from sanic.exceptions import abort


class UserManager:
    def __init__(self, base_url):
        self.url = base_url
        self.register = 'register'
        self.auth = 'authenticate'

    async def authenticate_user(self, username, session):
        return await self._wrap_request(session, username,
                                        {'endpoint': self.auth,
                                         'key': 'valid'})

    async def register_user(self, username, session):
        return await self._wrap_request(session, username,
                                        {'endpoint': self.register,
                                         'key': 'success'})

    async def _wrap_request(self, session, username, meta):
        async with session.get('{}/{}/{}'.format(self.url, meta['endpoint'], username)) as resp:
            return await self._is_response_valid(resp, meta['key'])

    async def _is_response_valid(self, response, key):
        if response.status == HTTPStatus.OK:
            content = await response.json()
            return content[key]
        abort(response.status)
