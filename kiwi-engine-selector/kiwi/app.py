from collections import namedtuple

from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from aiohttp import ClientSession

from kiwi.selector.select_recommender import get_pictures

User = namedtuple('User', 'name')

app = Sanic(__name__)

@app.post('/images')
async def test(request: Request):
    post_json = request.json
    user = User(**post_json['user'])
    with ClientSession() as session:
        pics = await get_pictures(session, user)
        return json({"picures": pics})




app.run(host="0.0.0.0", port=8000, debug=True)