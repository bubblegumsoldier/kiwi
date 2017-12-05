from os import environ
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from aiohttp import ClientSession

from kiwi.config import APP_CONFIG, CONTENT_CONFIG, RECOMMENDERS
from kiwi.selector.Types import User, Voting
from kiwi.selector.RecommenderSelector import RecommenderSelector
from kiwi.enricher.Enricher import Enricher

app = Sanic(__name__)
selector = RecommenderSelector.from_config(RECOMMENDERS)


@app.post('/recommendation')
async def images(request: Request):
    post_json = request.json
    user = User(**post_json['user'])
    async with ClientSession() as session:
        response = await selector.get_recommendations(session, user)
        if response.json['unvoted'] <= CONTENT_CONFIG['unvoted_threshold']:
            await request_content()
        return json({'recommendations': {
            'user': response.json['user'],
            'posts': await Enricher().enrich(response.json['posts'])}})


@app.post('/content')
async def content(request: Request):
    async with ClientSession() as session:
        await selector.distribute_posts(session, request.json['posts'])
        return json({'accepted': True})


@app.post('/feedback')
async def feedback(request: Request):
    post_json = request.json
    voting = Voting(**post_json['feedback'])
    async with ClientSession() as session:
        await selector.distribute_vote(session, voting)
        return json({'accepted': True})


async def request_content():
    data = {'count': CONTENT_CONFIG['unvoted_threshold'],
            'return_url': build_url(**APP_CONFIG, endpoint='content')}
    async with ClientSession() as session:
        url = build_url(**CONTENT_CONFIG['address'])
        
        post = session.post(url, json=data)
        async with post as response:
            await response.text()

def build_url(**kwargs):
    return 'http://{host}:{port}/{endpoint}'.format_map(kwargs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_CONFIG['port'])
