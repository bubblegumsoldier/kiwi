from http import HTTPStatus
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic.config import LOGGING
from kiwi.recommender.recommend import (recommend_for, store_feedback,
                                        add_content)
from kiwi.Logging import setup_logging, log_exception

app = Sanic(__name__)


def return_exception_as_json(exceptions=(Exception)):
    def decorator(func):
        async def helper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                return json({"error": e.args},
                            HTTPStatus.INTERNAL_SERVER_ERROR)
        return helper
    return decorator


@app.get('/recommendation')
@return_exception_as_json()
@log_exception()
async def recommend(request: Request):
    args = request.raw_args
    pictures = await recommend_for(args["user"], int(args.get("count", 10))) 
    return json(pictures)


@app.post('/feedback')
@return_exception_as_json()
@log_exception()
async def feedback(request: Request):
    vote_info = await store_feedback(request.json['vote'])
    return json(vote_info)


@app.post('/content')
@return_exception_as_json()
@log_exception()
async def add_posts(request: Request):
    inserted_info = await add_content(request.json['posts'])
    return json(inserted_info)


setup_logging()
app.run(host="0.0.0.0", port=8901, debug=True, log_config=LOGGING)
