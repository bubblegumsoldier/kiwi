from http import HTTPStatus
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from aiomysql import create_pool
from kiwi.recommender.Recommender import Recommender
from kiwi.database.DataAccessor import DataAccessor
from kiwi.config import read_app_config, read_mysql_config
from kiwi.Types import Vote

app = Sanic(__name__)


@app.listener('before_server_start')
async def setup(sanic, loop):
    pool = await create_pool(**read_mysql_config()._asdict(),
                             autocommit=True,
                             loop=loop,
                             pool_recycle=600)
    sanic.pool = pool


@app.listener('after_server_stop')
async def teardown(sanic, loop):
    sanic.pool.close()
    await sanic.pool.wait_closed()


@app.get('/recommendation')
async def recommend(request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user}
    '''
    args = request.raw_args
    async with app.pool.acquire() as conn:
        accessor = DataAccessor(conn)
        recommender = Recommender(accessor)
        pictures = await recommender.recommend_for(args['user'],
                                                   int(args.get('count', 10)))
        return json(pictures)


@app.post('/feedback')
async def feedback(request: Request):
    '''
    Stores feedback in form {vote: {user, post, vote}}
    Returns {user, unvoted} if successful.
    Returns {} with Error Code 500 (Internal Server Error) if unsuccessful
    '''
    async with app.pool.acquire() as conn:
        accessor = DataAccessor(conn)
        recommender = Recommender(accessor)

        vote_info = await recommender.store_feedback(
            Vote(**request.json['vote']))
        if vote_info:
            return json(vote_info)
        return json({}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.post('/content')
async def add_posts(request: Request):
    '''
    Stores new content in form {posts: post[]}
    Returns {inserted_count}.
    If single posts cannot be inserted, due to duplication returns the 
    actually inserted count.
    '''
    async with app.pool.acquire() as conn:
        accessor = DataAccessor(conn)
        recommender = Recommender(accessor)

        inserted_info = await recommender.add_content(request.json['posts'])
        return json(inserted_info)

@app.get('/activation')
async def activation(request: Request):
    '''
    Returns the activation value for the given set of heuristics
    '''
    heuristics = request.json['heuristics']
    return json({"activation": 0, 'received_heuristics': heuristics})

if __name__ == '__main__':
    app.run(**read_app_config()._asdict())
