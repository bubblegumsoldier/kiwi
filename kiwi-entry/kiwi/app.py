from http import HTTPStatus
from sanic import Sanic
from sanic.response import json 
from sanic.request import Request
from sanic.exceptions import abort
from aiohttp import ClientSession
from kiwi.config import load_config
from kiwi.UserManager import UserManager
from kiwi.RecommenderRouter import RecommenderRouter

app = Sanic(__name__)

config = load_config()

user_manager = UserManager(base_url='{host}:{port}'
                           .format_map(config['user-manager'])
                           )

recommender_router = RecommenderRouter(url='{}:{}'
                                       .format_map(config['recommender-router']))


@app.listener('before_server_start')
def init(app: Sanic, loop):
    app.http_session = ClientSession(loop=loop)


@app.get('/recommendation/<user>')
@app.get('/recommendation/<user>/<count>')
async def recommendation(request, user, count):
    with app.http_session as session:
        is_valid_user = user_manager.authenticate_user(user, session)
        if is_valid_user:
            return recommender_router.recommend(session, user, count)
        return json({'error': 'user is not registere'}, HTTPStatus.UNAUTHORIZED)


@app.post('/feedback')
async def feedback(request: Request):
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST)
    async with app.http_session as session:
        user = request.json['feedback']['user']
        is_valid_user = await user_manager.authenticate_user(user, session)
        if is_valid_user:
            response = await recommender_router.feedback(session, request.json)
            return json({}, status=HTTPStatus.ACCEPTED)

@app.post('/user/<user>')
async def register(request, user):
    if not user:
        return json({'error': 'no username provided'}, HTTPStatus.BAD_REQUEST)
    with app.http_session as session:
        registration = await user_manager.register_user(user, session)
        if registration:
            return json({'user': user}, HTTPStatus.CREATED)
        return json({'user': user}, HTTPStatus.CONFLICT)


