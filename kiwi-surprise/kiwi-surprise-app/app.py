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
from TransferTypes import create_vote


app = Sanic(__name__)


async def periodic_retrain():
    app.run_retrain = True
    await sleep(30)
    while app.run_retrain:
        getLogger('root').info("Retraining...")
        loop = app.loop
        new_accessor = await loop.run_in_executor(
            app.pool,
            app.accessor.with_updated_trainset,
            app.accessor.df,
            app.accessor.new_voted,
            app.accessor.trainset.rating_scale)
        new_predictor = Algorithm(loop, app.pool, create_algorithm())
        await new_predictor.fit(new_accessor.trainset)
        app.predictor = new_predictor
        app.accessor = new_accessor
        getLogger('root').info('Retraining finished...')
        await sleep(30)


@app.listener("before_server_start")
async def setup(app, loop):
    app.pool = ProcessPoolExecutor()
    app.predictor = Algorithm(loop, app.pool, create_algorithm())
    accessor = DataAccessor()
    await app.predictor.fit(accessor.trainset)
    app.accessor = accessor


@app.listener("before_server_stop")
async def teardown(app, loop):
    app.run_retrain = False
    app.pool.shutdown()


@app.get('/recommendation')
async def recommend(request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user}    
    '''
    args = request.raw_args
    getLogger('root').info(
        'Received recommendation request for {}'.format(args['user']))
    recommender = Recommender(app.predictor, app.accessor)
    posts = await recommender.recommend_for(int(args['user']),
                                            int(args.get('count', 10)))
    return json(posts)


@app.post('/feedback')
async def feedback(request: Request):
    vote = request.json['vote']
    recommender = Recommender(app.predictor, app.accessor)
    vote_result = await recommender.store_feedback(create_vote(vote))
    return json(vote_result)


@app.post('/content')
async def content(request: Request):
    recommender = Recommender(app.predictor, app.accessor)
    inserted_items = recommender.add_content(request.json['posts'])
    return json(inserted_items)


if __name__ == '__main__':
    app.add_task(periodic_retrain)
    app.run(host='0.0.0.0', port=5001)
