from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic.config import LOGGING
from kiwi.recommender.recommend import (recommend_for, store_feedback,
                                        add_content)
from kiwi.Logging import setup_logging, log_exception
from kiwi.exception_handling import return_exception_as_json
from kiwi.config import read_app_config

app = Sanic(__name__)


@app.get('/recommendation')
@return_exception_as_json()
@log_exception()
async def recommend(request: Request):
    '''
    Gets recommendations for user
    Expects args in query string form -> user=x&count=n
    Returns json object {posts, unvoted, user}
    '''
    args = request.raw_args
    pictures = await recommend_for(args['user'], int(args.get('count', 10)))
    return json(pictures)


@app.post('/feedback')
@return_exception_as_json()
@log_exception()
async def feedback(request: Request):
    '''
    Stores feedback in form {vote: {user, post, vote}}
    Returns {user, unvoted}
    '''
    vote_info = await store_feedback(request.json['vote'])
    return json(vote_info)


@app.post('/content')
@return_exception_as_json()
@log_exception()
async def add_posts(request: Request):
    '''
    Stores new content in form {posts: post[]}
    Returns {inserted_count}
    '''
    inserted_info = await add_content(request.json['posts'])
    return json(inserted_info)


setup_logging()

app.run(**read_app_config()._asdict(), log_config=LOGGING)
