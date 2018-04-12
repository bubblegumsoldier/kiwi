from http import HTTPStatus
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from aiomysql import create_pool
from kiwi.recommender.Recommender import Recommender
from kiwi.database.DataAccessor import DataAccessor
from kiwi.config import (read_app_config, read_mysql_config,
                         read_rating_config, get_sql_statements)
from kiwi.Types import Vote

app = Sanic('latest-recommender')
rating_config = read_rating_config()
SQL_STMTS = get_sql_statements()


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


@app.middleware("request")
async def generate_accessor(request):
    app.conn = await app.pool.acquire()
    app.accessor = DataAccessor(app.conn, SQL_STMTS)
    app.recommender = Recommender(app.accessor, **rating_config)


@app.middleware("response")
async def teardown_accessor(request, response):
    app.conn.close()
    await app.conn.ensure_closed()
    await app.pool.release(app.conn)


@app.get('/recommendation')
async def recommend(request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user}
    '''
    args = request.raw_args
    recommendations = await app.recommender.recommend_for(args['user'],
                                                          int(args.get('count', 10)))
    return json(recommendations)


@app.post('/feedback')
async def feedback(request: Request):
    '''
    Stores feedback in form {vote: {user, post, vote}}
    Returns {user, unvoted} if successful.
    Returns {} with Error Code 500 (Internal Server Error) if unsuccessful
    '''

    vote_info = await app.recommender.store_feedback(
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
    inserted_info = await app.recommender.add_content(request.json['posts'])
    return json(inserted_info)


@app.post('/training')
async def add_votes(request: Request):
    '''
    Expects votes as json {votes: [vote]}
    vote -> {user post vote}
    '''
    votes = request.json['votes']
    inserted_user = await app.accessor.batch_register_users(
        {vote['user'] for vote in votes})
    inserted = await app.accessor.insert_votes(
        (vote['user'], vote['post'], vote['vote']) for vote in votes)
    return json({
        'inserted_users': inserted_user,
        'inserted_votes': inserted
    })


@app.get('/activation')
async def activation(request: Request):
    '''
    Returns the activation value for the given set of heuristics
    '''
    heuristics = request.json['heuristics']
    return json({"activation": 100, 'received_heuristics': heuristics})


@app.get('/predict')
async def predict(request: Request):
    user = request.raw_args['user']
    item = request.raw_args['item']
    prediction = await app.recommender.predict_for(user, item)
    return json(prediction)


if __name__ == '__main__':
    config = read_app_config()._asdict()
    print(config)
    app.run(host='0.0.0.0', port=8000)
