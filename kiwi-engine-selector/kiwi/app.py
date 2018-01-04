from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from aiohttp import ClientSession

from kiwi.config import APP_CONFIG, CONTENT_CONFIG, RECOMMENDERS
from kiwi.selector.Types import RecommendationRequest, Voting
from kiwi.selector.RecommenderSelector import RecommenderSelector
from kiwi.enricher.Enricher import Enricher
from kiwi.database.MongoConnection import get_connection

app = Sanic(__name__)
selector = RecommenderSelector.from_config(RECOMMENDERS)


@app.post('/recommendation')
async def images(request: Request):
    post_json = request.json
    recommendation_request = RecommendationRequest(**post_json)
    response = await selector.get_recommendations(app.client_session,
                                                  recommendation_request)
    if response.json['unvoted'] <= CONTENT_CONFIG['unvoted_threshold']:
        print(
            '{user} has {count} unvoted posts remaining. Requesting content'.format(
                user=response.json['user'],
                count=response.json['unvoted']))

        await request_content()
    return json({'recommendations': {
        'user': response.json['user'],
        'posts': await Enricher(app.mongo_connection).enrich(
            response.json['posts'])}})


@app.post('/content')
async def content(request: Request):
    await selector.distribute_posts(app.client_session, request.json['posts'])
    return json({'accepted': True})


@app.post('/feedback')
async def feedback(request: Request):
    post_json = request.json
    voting = Voting(**post_json['feedback'])
    await selector.distribute_vote(app.client_session, voting)
    return json({'accepted': True})


async def request_content():
    data = {'count': CONTENT_CONFIG['unvoted_threshold'],
            'return_url': build_url(**APP_CONFIG, endpoint='content')}
    url = build_url(**CONTENT_CONFIG['address'])

    post = app.client_session.post(url, json=data)
    async with post as response:
        await response.text()


def build_url(**kwargs):
    return 'http://{host}:{port}/{endpoint}'.format_map(kwargs)


@app.listener('before_server_start')
def init(app, loop):
    app.mongo_connection = get_connection()
    app.client_session = ClientSession(loop=loop)


@app.listener('after_server_stop')
async def teardown(app, loop):
    app.mongo_connection.close()
    await app.client_session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_CONFIG['port'])
