from aiohttp.client import ClientSession
from kiwi.selector.Types import Voting, Response, RecommendationRequest

TEMPLATE = '{base}/{endpoint}'


class Recommender:
    def __init__(self, address):
        self.base = address

    @classmethod
    def from_config(cls, address):
        self = Recommender(address)
        return self

    async def get_content_for_user(self, session: ClientSession,
                                   request: RecommendationRequest):
        url = self._format_template('recommendation')
        session = session.get(url, params=request._asdict())
        return await self._get_response(session)

    async def predict_for(self, session, user, item):
        url = self._format_template('prediction')
        response = session.get(url, params={'user': user, 'item': item})
        return await self._get_response(response)

    async def send_feedback(self, session: ClientSession, voting: Voting):
        url = self._format_template('feedback')
        session = session.post(url, json={'vote': voting._asdict()})
        return await self._get_response(session)


    async def push_votes(self, session, votes):
        url = self._format_template('training')
        session = session.post(url, json=votes)
        return await self._get_response(session)

    async def push_content(self, session: ClientSession, posts):
        url = self._format_template('content')
        session = session.post(url, json={'posts': posts})
        return await self._get_response(session)

    async def get_activation(self, session: ClientSession, heuristics):
        url = self._format_template('activation')
        param_dict = dict(heuristics=heuristics)
        session = session.get(url, json=param_dict)
        response = await self._get_response(session)
        return response.json["activation"]

    async def _get_response(self, session):
        async with session as response:
            if response.status != 200:
                return Response(status=response.status, json={})
            return Response(status=response.status,
                            json=await response.json())

    def _format_template(self, endpoint):
        return TEMPLATE.format(base=self.base, endpoint=endpoint)
