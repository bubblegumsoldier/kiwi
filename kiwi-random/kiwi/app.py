import asyncio
from os import environ
from sanic import Sanic
from sanic.request import Request
from sanic.response import json, text
from kiwi.Types import User, Vote
from kiwi.recommender.recommend import recommend_for, insert_vote, add_content

app = Sanic(__name__)


@app.post('/recommend')
async def recommend(request: Request):
    user = User(**request.json['user']) # add validation
    pictures = await recommend_for(user)
    return json(pictures)


@app.post('/feedback')
async def feedback(request: Request):
    vote = Vote(**request.json['vote']) # add validation
    await insert_vote(vote)
    return json(vote)

@app.post('/posts')
async def add_posts(request: Request):
    inserted = await add_content(request.json['posts'])
    return json(inserted)

app.run(host="0.0.0.0", port=8901, debug=True)