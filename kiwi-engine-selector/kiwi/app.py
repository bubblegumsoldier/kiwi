from collections import namedtuple
from json import dumps
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from aiohttp import ClientSession

from kiwi.selector.select_recommender import get_pictures, distribute_content

User = namedtuple('User', 'name')

app = Sanic(__name__)


@app.post('/images')
async def images(request: Request):
    post_json = request.json
    user = User(**post_json['user'])
    async with ClientSession() as session:
        response = await get_pictures(session, user)

        if response["unvoted"] < 50:
            print("Requesting content")
            await request_content()

        return json({"pictures": response})


@app.post('/content')
async def content(request: Request):
    post_json = request.json
    async with ClientSession() as session:
        await distribute_content(session, post_json["posts"])
        return json("OK")


async def request_content():
    data = {"count": 50, "return_url": "http://localhost:8000/content"}
    async with ClientSession() as session:
        post = session.post('http://localhost:7000/items', json=data)
        async with post as response:
            res = await response
            print(res)





app.run(host="0.0.0.0", port=8000, debug=True)
