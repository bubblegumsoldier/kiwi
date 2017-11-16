from json import dumps
from collections import namedtuple
from aiohttp.client import ClientSession

Voting = namedtuple('Voting', 'user product vote')
Endpoints = namedtuple('Endpoints', 'pics feedback')

template = '{base}/{endpoint}'

#could have some "is_applicable" method, that gives hints when to use the instance.
class Recommender:
    def __init__(self, base_url, endpoints: Endpoints):
        self.base = base_url
        self.endpoints = endpoints

    async def get_pics_for_user(self, session: ClientSession, user):
        url = template.format(base=self.base,
                              endpoint=self.endpoints.pics)
        async with session.post(url, json={"user":user.name}) as response:
            return await response.json()

    async def send_feedback(self, session: ClientSession, voting: Voting):
        url = template.format(base=self.base, endpoint=self.endpoints.feedback)
        async with session.post(url, json=dumps(voting)):
            return
