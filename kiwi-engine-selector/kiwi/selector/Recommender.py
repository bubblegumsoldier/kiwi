from collections import namedtuple
from aiohttp.client import ClientSession

Voting = namedtuple('Voting', 'user product vote')
Endpoints = namedtuple('Endpoints', 'recommend feedback content')

template = '{base}/{endpoint}'

# could have some "is_applicable" method, that gives hints when to use the instance.


class Recommender:
    def __init__(self, base_url, endpoints: Endpoints):
        self.base = base_url
        self.endpoints = endpoints

    def _format_template(self, endpoint):
        return template.format(base=self.base, endpoint=endpoint)

    async def get_pics_for_user(self, session: ClientSession, user):
        url = self._format_template(self.endpoints.recommend)
        session = session.get(url,
                              params={"user": user.name, "count": 10})
        async with session as response:
            return await response.json()

    async def send_feedback(self, session: ClientSession, voting: Voting):
        url = self._format_template(self.endpoints.feedback)
        async with session.post(url, json={"vote": voting}):
            return

    async def push_content(self, session: ClientSession, posts):
        url = self._format_template(self.endpoints.content)
        async with session.post(url, json={"posts": posts}) as response:
            res = await response.json()
            print(res)