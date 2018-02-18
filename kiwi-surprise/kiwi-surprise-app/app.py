from concurrent.futures import ProcessPoolExecutor
from asyncio import sleep
from logging import getLogger
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from database.DataAccessor import DataAccessor
from Algorithm import Algorithm
from Recommender import Recommender
from config import create_algorithm
from TransferTypes import Vote


app = Sanic(__name__)


@app.listener("before_server_start")
async def setup(app, loop):
    app.surprise_algo = create_algorithm()
    app.pool = ProcessPoolExecutor()
    app.predictor = Algorithm(loop, app.pool, app.surprise_algo)
    accessor = DataAccessor()
    await app.predictor.fit(accessor.trainset)
    app.accessor = accessor


@app.get('/recommendation')
async def recommend(request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user}
    '''
    args = request.raw_args
    getLogger('root').info('Received recommendation request for {}'.format(args['user']))
    recommender = Recommender(app.predictor, app.accessor)
    posts = await recommender.recommend_for(int(args['user']),
                                               int(args.get('count', 10)))
    return json(posts)


@app.post('/feedback')
async def feedback(request: Request):
    vote = request.json['vote']
    recommender = Recommender(app.predictor, app.accessor)
    vote_result = await recommender.store_feedback(Vote(**vote))
    return json(vote_result)


@app.post ('/content')
async def content(request: Request):
    recommender = Recommender(app.predictor, app.accessor)
    inserted_items = recommender.add_content(request.json['posts'])
    return json(inserted_items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
