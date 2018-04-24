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


@app.get('/recommendation')
async def images(request: Request):
    """
    Gets recommendations from a chosen Recommender.
    Expects url parameters: user, count
    """
    recommendation_request = RecommendationRequest(**request.raw_args)
    response = await selector.get_recommendations(app.client_session,
                                                  recommendation_request)
    return json(response.json, status=response.status)


@app.post('/content')
async def content(request: Request):
    """
    Distributes content to all registered recommenders. 
    If one recommender has an error, this method will return status 500.
    The erroring recommender will be logged.
    Expects json object with: {posts: [post]}.
    The required setup of post depends on the recommenders.
    Minimum is {id: string|int}
    """
    response = await selector.distribute_posts(app.client_session,
                                               request.json['posts'])
    if not response:
        return json({}, status=500)
    return json({'accepted': True})


@app.post('/feedback')
async def feedback(request: Request):
    """
    Distributes feedback of the user to all recommenders.
    Feedback should have shape: {vote: {user, post, vote}}
    """
    post_json = request.json
    voting = Voting(**post_json['vote'])
    await selector.distribute_vote(app.client_session, voting)
    return json({'accepted': True})


@app.get('/predict')
async def predict(request: Request):
    """
    Excepts url parameters: user=..., item=...
    Returns predicted score for this user/item combination.
    """
    user = request.raw_args['user']
    item = request.raw_args['item']
    prediction = await selector.predict_for(app.client_session, user, item)
    print(prediction)
    return json(prediction.json, status = prediction.status)


@app.post('/training')
async def train(request: Request):
    """
    Expects json with {votes: [vote]}
    Where vote -> {user post vote}
    Should simplify and speedup training process
    """
    training = await selector.distribute_votes(app.client_session, request.json)
    return json(training)


@app.listener('before_server_start')
def init(sanic, loop):
    sanic.client_session = ClientSession(loop=loop)


@app.listener('after_server_stop')
async def teardown(sanic, loop):
    await sanic.client_session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_CONFIG['port'])
