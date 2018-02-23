from concurrent.futures import ThreadPoolExecutor, CancelledError
from aiomysql import create_pool
from asyncio import sleep
from logging import getLogger
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from kiwi.database.DataAccessor import DataAccessor
from kiwi.Algorithm import Algorithm
from kiwi.Recommender import Recommender
from kiwi.config import create_algorithm, read_mysql_config
from kiwi.TransferTypes import create_vote


app = Sanic(__name__)


def create_accessor(context):
    return DataAccessor(conn=context)
    # return BuiltinDataAccessor(context=context)


# def create_pool(*args, **kwargs):
#     return BuiltinContext()


async def periodic_retrain():
    await sleep(30)
    while app.run_retrain:
        getLogger('root').info("Retraining...")
        loop = app.loop
        async with app.pool.acquire() as conn:
            accessor = create_accessor(conn)
            new_predictor = Algorithm(
                loop, app.executor, create_algorithm())
            await new_predictor.fit(await accessor.trainset())
            app.predictor = new_predictor
            getLogger('root').info('Retraining finished...')
            await sleep(30)


@app.listener("before_server_start")
async def setup(context, loop):
    context.executor = ThreadPoolExecutor()
    context.predictor = Algorithm(loop, context.executor, create_algorithm())
    context.pool = await create_pool(
        **read_mysql_config()._asdict(),
        autocommit=True,
        loop=loop,
        pool_recycle=600)

    async with context.pool.acquire() as conn:
        accessor = create_accessor(conn)
        await context.predictor.fit(
            await accessor.trainset(rating_scale=(0, 1)))


@app.middleware("request")
async def generate_accessor(request):
    app.conn = await app.pool.acquire()
    app.accessor = create_accessor(app.conn)


@app.middleware("response")
async def teardown_accessor(request, response):
    app.conn.close()


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
    getLogger('root').info(
        'Received recommendation request for %s', args['user'])
    recommender = Recommender(app.predictor, app.accessor)
    posts = await recommender.recommend_for(args['user'],
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
    app.run_retrain = True
    app.run(host='0.0.0.0', port=5001)
