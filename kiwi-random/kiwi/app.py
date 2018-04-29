from http import HTTPStatus
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from aiomysql import create_pool
from kiwi.recommender.Recommender import Recommender
from kiwi.database.DataAccessor import DataAccessor
from kiwi.config import read_app_config, read_mysql_config, get_rating_config
from kiwi.Types import Vote

from kiwi.recommender.ActivationCalculator import ActivationCalculator


app = Sanic(__name__)
rating_config = get_rating_config()


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
    request['conn'] = await app.pool.acquire()
    request['accessor'] = DataAccessor(request['conn'])
    request['recommender'] = Recommender(request['accessor'], **rating_config)


@app.middleware("response")
async def teardown_accessor(request, response):
    await request['conn'].ensure_closed()
    app.pool.release(request['conn'])


@app.get('/recommendation')
async def recommend(request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user}
    '''
    args = request.raw_args
    pictures = await request['recommender'].recommend_for(args['user'],
                                                          int(args.get('count', 10)))
    return json(pictures)


@app.post('/feedback')
async def feedback(request: Request):
    '''
    Stores feedback in form {vote: {user, post, vote}}
    Returns {user, unvoted} if successful.
    Returns {} with Error Code 500 (Internal Server Error) if unsuccessful
    '''
    vote_info = await request['recommender'].store_feedback(
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

    inserted_info = await request['recommender'].add_content(request.json['posts'])
    return json(inserted_info)


@app.get('/activation')
async def activation(request: Request):
    '''
    Returns the activation value for the given set of heuristics
    '''
    heuristics = request.json['heuristics']
    ac = ActivationCalculator(heuristics, request['accessor'])
    activation = await ac.get_activation()
    return json({"activation": activation, 'received_heuristics': heuristics})


@app.get('/predict')
async def predict(request):
    user = request.raw_args['user']
    item = request.raw_args['item']
    return json(await request['recommender'].predict_for(user, item))


@app.post('/training')
async def add_votes(request: Request):
    '''
    Expects votes as json {votes: [vote]}
    vote -> {user post vote}
    '''
    votes = request.json['votes']
    inserted_user = await request['accessor'].batch_register_users(
        {vote[0] for vote in votes})
    inserted = await request['accessor'].insert_votes(votes)
    return json({
        'inserted_users': inserted_user,
        'inserted_votes': inserted
    })

if __name__ == '__main__':
    app.run(**read_app_config()._asdict())
