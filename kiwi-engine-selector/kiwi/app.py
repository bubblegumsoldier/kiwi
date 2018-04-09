from logging import getLogger
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from aiohttp import ClientSession
from kiwi.config import APP_CONFIG, RECOMMENDERS
from kiwi.selector.Types import RecommendationRequest, Voting
from kiwi.selector.RecommenderSelector import RecommenderSelector

app = Sanic(__name__)
selector = RecommenderSelector.from_config(RECOMMENDERS)


@app.post('/recommendation')
async def images(request: Request):
    post_json = request.json
    recommendation_request = RecommendationRequest(**post_json)
    response = await selector.get_recommendations(app.client_session,
                                                  recommendation_request)
    return response


@app.post('/content')
async def content(request: Request):
    response = await selector.distribute_posts(app.client_session,
                                               request.json['posts'])
    if response.status == 500:
        return json({}, status=500)
    return json({'accepted': True})


@app.post('/feedback')
async def feedback(request: Request):
    post_json = request.json
    voting = Voting(**post_json['feedback'])
    await selector.distribute_vote(app.client_session, voting)
    return json({'accepted': True})

@app.listener('before_server_start')
def init(sanic, loop):
    sanic.client_session = ClientSession(loop=loop)


@app.listener('after_server_stop')
async def teardown(sanic, loop):
    await sanic.client_session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_CONFIG['port'])
