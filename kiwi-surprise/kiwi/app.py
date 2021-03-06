from concurrent.futures import ThreadPoolExecutor, CancelledError
from aiomysql import create_pool
from asyncio import sleep, ensure_future
from functools import partial
from logging import getLogger
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from kiwi.database.DataAccessor import DataAccessor
from kiwi.Algorithm import AlgorithmWrapper
from kiwi.Recommender import Recommender
import kiwi.config as config
from kiwi.TransferTypes import create_vote
from pymysql.err import OperationalError


app = Sanic(__name__)

retrain_config = config.set_retraining_cycle()
rating_scale = config.read_rating_config()
algorithm_module = config.get_algorithm_config()


async def repeated_pool(loop, sleeper, tries):
    n = 1
    while n <= tries:
        try:
            return await create_pool(**config.read_mysql_config()._asdict(),
                                     autocommit=True,
                                     loop=loop,
                                     pool_recycle=600)
        except OperationalError as e:
            getLogger('root').warn(e)
            getLogger('root').warn("Waiting {}s before retry".format(sleeper))
            await sleep(sleeper)
            n += 1

    return await create_pool(**config.read_mysql_config()._asdict(),
                             autocommit=True,
                             loop=loop,
                             pool_recycle=600)


async def periodic_retrain(period):
    await sleep(period)
    while app.run_retrain:
        await retrain(app)
        await sleep(period)


async def retrain(app):
    getLogger('root').info("Retraining...")
    loop = app.loop
    async with app.pool.acquire() as conn:
        accessor = DataAccessor(conn=conn, rating_scale=rating_scale)
        new_predictor = AlgorithmWrapper(
            loop, app.executor, algorithm_module.create_algorithm())
        await new_predictor.fit(await accessor.trainset())
        app.predictor = new_predictor
        getLogger('root').info('Retraining finished...')


@app.listener("before_server_start")
async def setup(context, loop):
    context.executor = ThreadPoolExecutor()
    context.predictor = AlgorithmWrapper(
        loop, context.executor, algorithm_module.create_algorithm())
    context.pool = await repeated_pool(loop, 5, 10)

    async with context.pool.acquire() as conn:
        accessor = DataAccessor(conn=conn, rating_scale=rating_scale)
        trainset = await accessor.trainset()
        await context.predictor.fit(trainset)


@app.middleware("request")
async def generate_accessor(request):
    request['conn'] = await app.pool.acquire()
    request['accessor'] = DataAccessor(
        conn=request['conn'], rating_scale=rating_scale)


@app.middleware("response")
async def teardown_accessor(request: Request, response):
    if request.path in retrain_config.get('on_request', []):
        ensure_future(retrain(app))
    if request.path == "/training" and request.json.get('retrain', False):
        ensure_future(retrain(app))
    await request['conn'].ensure_closed()
    app.pool.release(request['conn'])


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
    Returns json object {posts, unvoted, user}    
    '''
    args = request.raw_args
    recommender = Recommender(app.predictor, request['accessor'])
    posts = await recommender.recommend_for(args['user'],
                                            int(args.get('count', 10)))
    return json(posts)


@app.post('/feedback')
async def feedback(request: Request):
    '''Stores the feedback for a recommended post. Will return a information object on success and an empty object on failure. 
    Think about returning 409-Conflict on failure instead, because the empty object can cause an issue in engine service.'''
    vote = request.json['vote']
    recommender = Recommender(app.predictor, request['accessor'])
    vote_result = await recommender.store_feedback(create_vote(vote))
    return json(vote_result)


@app.post('/content')
async def content(request: Request):
    '''
    Inserts posts into the database. The request needs the format 
    { "posts": [{"id": string}]}.
    Returns the amout of inserted items and 200-OK.
        '''
    recommender = Recommender(app.predictor, request['accessor'])
    inserted_items = await recommender.add_content(request.json['posts'])
    return json(inserted_items)


@app.get('/predict')
async def predict(request: Request):
    user = request.raw_args['user']
    item = request.raw_args['item']
    recommender = Recommender(app.predictor, request['accessor'])
    predictions = await recommender.predict_for(user, item)
    return json(predictions)


@app.post('/training')
async def training(request: Request):
    votes = request.json['votes']
    inserted_user = await request['accessor'].batch_register_users(
        {vote[0] for vote in votes})
    inserted = await request['accessor'].insert_votes(votes)
    return json({
        'inserted_users': inserted_user,
        'inserted_votes': inserted})


@app.get('/activation')
async def activation(request: Request):
    '''
    Returns the activation value for the given set of heuristics
    '''
    heuristics = request.json['heuristics']
    a = await algorithm_module.get_activation(heuristics, request['accessor'], app.predictor)

    return json({"activation": a, 'received_heuristics': heuristics})

if __name__ == '__main__':
    app.run_retrain = True
    if retrain_config['periodic']:
        print("Periodic training enabled")
        app.add_task(partial(periodic_retrain, retrain_config['periodic']))
    app.run(host='0.0.0.0', port=8000)
