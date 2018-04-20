from concurrent.futures import ThreadPoolExecutor, CancelledError
from aiomysql import create_pool
from asyncio import ensure_future, gather
from logging import getLogger
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import abort
from kiwi.database.DataAccessor import DataAccessor
from kiwi.Recommender import Recommender
from kiwi.config import read_mysql_config, read_config
from kiwi.TransferTypes import create_vote
from kiwi.AsyncContentWrapper import AsyncContentWrapper
from kiwi.ContentEngine import ContentEngine
from kiwi.ActivationCalculator import ActivationCalculator
import time

app = Sanic(__name__)


def create_accessor(context):
    return DataAccessor(conn=context)


async def retrain(context, loop):
    print("Start training...")
    start = time.time()
    async with context.pool.acquire() as conn:
        accessor = create_accessor(conn)
        content_frame = await accessor.get_content_frame()
        rating_frame = await accessor.get_vote_frame()
    print("Collected data in {}".format(time.time() - start))
    algorithm = ContentEngine(
        content_frame,
        rating_frame)
    predictor = AsyncContentWrapper(
        loop, context.executor, algorithm)
    await predictor.fit()
    print("Completed training in {}s".format(time.time() - start))
    context.algorithm = algorithm
    context.predictor = predictor


@app.listener("before_server_start")
async def setup(context, loop):
    context.executor = ThreadPoolExecutor()

    context.pool = await create_pool(
        **read_mysql_config()._asdict(),
        autocommit=True,
        loop=loop,
        pool_recycle=120)

    await retrain(context, loop)


@app.middleware("request")
async def generate_accessor(request):
    app.conn = await app.pool.acquire()
    app.accessor = create_accessor(app.conn)


@app.middleware("response")
async def teardown_accessor(request, response):
    app.conn.close()
    await app.conn.ensure_closed()
    await app.pool.release(app.conn)


@app.listener("before_server_stop")
async def teardown(context, loop):
    context.run_retrain = False
    context.executor.shutdown()
    context.pool.close()
    await context.pool.wait_closed()


@app.get('/recommendation')
async def recommend(request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user, meta}
    '''
    args = request.raw_args
    recommender = Recommender(
        app.predictor, app.accessor, read_config())
    posts = await recommender.recommend_for(args['user'],
                                            int(args.get('count', 10)))
    return json(posts)


@app.post('/feedback')
async def feedback(request: Request):
    '''Stores the feedback for a recommended post. Will return a information object on success and an empty object on failure.
    Think about returning 409-Conflict on failure instead, because the empty object can cause an issue in engine service.'''
    vote = request.json['vote']
    config = read_config()
    recommender = Recommender(
        app.predictor, app.accessor, config)
    try:
        vote_result = await recommender.store_feedback(
            create_vote(vote, config['positive_cutoff']))
        return json(vote_result)
    except KeyError:
        abort(400, "Unknown user")

@app.post('/content')
async def content(request: Request):
    '''
    Inserts posts into the database. The request needs the format
    { "posts": [{"id": string, "tags": string}]}.
    Returns the amout of inserted items and 200-OK.
        '''
    filtered_posts = [(post['id'], post['tags'])
                      for post in request.json['posts']]
    inserted = await app.accessor.add_content(filtered_posts)
    if inserted > 0:
        ensure_future(retrain(app, app.loop))
    return json({"inserted_count": inserted})


@app.get('/predict')
async def predict(request: Request):
    recommender = Recommender(
        app.predictor, app.accessor, read_config())
    user = request.raw_args['user']
    item = request.raw_args['item']
    result = await recommender.predict(user, item)
    return json(result)


@app.get('/activation')
async def activation(request: Request):
    '''
    Returns the activation value for the given set of heuristics
    '''
    heuristics = request.json['heuristics']
    try:
        utv = app.predictor.get_user_taste_vector(heuristics["user"])
    except Exception:
        utv = None
    
    ac = ActivationCalculator(heuristics, app.accessor)
    a = await ac.get_activation(utv)

    return json({"activation": a, 'received_heuristics': heuristics})


@app.post('/training')
async def training(request: Request):
    votes = request.json['votes']
    do_retrain = request.json.get('retrain', False)
    inserted_user = await app.accessor.batch_register_users(
        {vote['user'] for vote in votes})
    inserted = await app.accessor.insert_votes(
        (vote['user'], vote['post'], vote['vote']) for vote in votes)
    if do_retrain:
        ensure_future(retrain(app, app.loop))
    return json({
        'inserted_users': inserted_user,
        'inserted_votes': inserted})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
