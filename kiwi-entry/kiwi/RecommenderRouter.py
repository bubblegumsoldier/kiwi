from http import HTTPStatus
from sanic.exceptions import abort


class RecommenderRouter:
    def __init__(self, url):
        self.base_url = url

    async def recommend(self, session, user, count):
        url = '{}/{}'.format(self.base_url,
                             'recommendation')
        json = {'user': user, 'count': count}
        async with session.post(url, json=json) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            abort(response.status)


    async def feedback(self, session, feedback_data):
        url = '{}/{}'.format(self.base_url,
                             'feedback')
        async with session.post(url, json=feedback_data) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            abort(response.status)

    async def content(self, session, content_data):
        url = '{}/{}'.format(self.base_url, 'feedback')
        async with session.post(url, json=content_data) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            abort(response.status)

