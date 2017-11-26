from collections import namedtuple
from aiohttp.client import ClientSession
from kiwi.selector.Types import Voting, Endpoints, Response

TEMPLATE = '{base}/{endpoint}'


class Recommender:
    def __init__(self, address, endpoints: Endpoints):
        self.base = address
        self.endpoints = endpoints

    @classmethod
    def from_config(cls, config_dict):
        endpoints = Endpoints(**config_dict['endpoints'])
        self = Recommender(config_dict['address'], endpoints)
        return self

    def _format_template(self, endpoint):
        return TEMPLATE.format(base=self.base, endpoint=endpoint)

    async def get_pics_for_user(self, session: ClientSession, user):
        url = self._format_template(self.endpoints.recommendation)
        session = session.get(url, params={"user": user.name, "count": 10})
        return await self._get_response(session)

    async def send_feedback(self, session: ClientSession, voting: Voting):
        url = self._format_template(self.endpoints.feedback)
        session = session.post(url, json={"vote": voting._asdict()})
        return await self._get_response(session)

    async def push_content(self, session: ClientSession, posts):
        url = self._format_template(self.endpoints.content)
        session = session.post(url, json={"posts": posts})
        return await self._get_response(session)

    async def _get_response(self, session):
        async with session as response:
            return Response(status=response.status,
                            json=await response.json())
