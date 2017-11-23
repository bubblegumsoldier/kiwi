from http import HTTPStatus
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic.config import LOGGING
from kiwi.recommender.recommend import (recommend_for, store_feedback,
                                        add_content)
from kiwi.Logging import setup_logging

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


@app.get('/recommendation/<user>')
@app.get('/recommendation/<user>/<count>')
@return_exception_as_json()
async def recommend(request: Request, user, count=None):
    pictures = await (recommend_for(user, int(count))
                      if count
                      else recommend_for(user))
    return json(pictures)


@app.post('/feedback')
@return_exception_as_json()
async def feedback(request: Request):
    vote = await store_feedback(request.json['vote'])
    return json(vote)


@app.post('/content')
@return_exception_as_json()
async def add_posts(request: Request):
    inserted = await add_content(request.json['posts'])
    return json({"inserted": inserted})


setup_logging()
app.run(host="0.0.0.0", port=8901, debug=True, log_config=LOGGING)
