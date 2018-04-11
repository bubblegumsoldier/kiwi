from http import HTTPStatus
from logging import getLogger
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from sanic.exceptions import abort
from aiohttp import ClientSession
from kiwi.config import load_config, get_content_config
from kiwi.UserManager import UserManager
from kiwi.RecommenderRouter import RecommenderRouter
from kiwi.enricher.Enricher import Enricher
from kiwi.database.MongoConnection import get_connection
from sanic_cors import CORS, cross_origin

app = Sanic(__name__)
CORS(app, automatic_options=True)

config = load_config()
content_config = get_content_config()

user_manager = UserManager(base_url=config['user_service'])
recommender_router = RecommenderRouter(url=config['switcher_service'])


@app.listener('before_server_start')
def init(sanic: Sanic, loop):
    sanic.mongo_connection = get_connection()
    sanic.http_session = ClientSession(loop=loop)


@app.listener('after_server_stop')
async def teardown(sanic, loop):
    sanic.mongo_connection.close()
    await sanic.http_session.close()


@app.get('/recommendation/<user>')
@app.get('/recommendation/<user>/<count:int>')
async def recommendation(request, user: str, count=10):
    await validate_user(user)
    response = await recommender_router.recommend(app.http_session, user, count)
    unvoted = response['unvoted']
    await check_unvoted_count(unvoted, response['user'])

    return json({'recommendations': {
        'user': response['user'],
        'posts': await Enricher(app.mongo_connection).enrich(
            response['posts'])}})


@app.route('/feedback', methods=["POST"])
async def feedback(request: Request):
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST)
    user = request.json['feedback']['user']
    await validate_user(user)
    await recommender_router.feedback(app.http_session, {'vote': request.json['feedback']})
    return json({}, status=HTTPStatus.ACCEPTED)


@app.route('/users/<user>', methods=['GET', 'POST'])
async def user(request: Request, user: str):
    if not user:
        return json({'error': 'no username provided'}, HTTPStatus.BAD_REQUEST)

    if request.method == "GET":
        return json({'user': user}, await handle_users_get(user))
    return json({'user': user}, await handle_users_post(user))


@app.post('/content')
async def content(request: Request):
    response = await recommender_router.content(app.http_session,
                                                request.json)
    if response:
        return json({}, status=200)
    return json({}, status=500)


async def validate_user(user):    
    is_valid_user = await user_manager.authenticate_user(user, app.http_session)
    print("User validation: {}".format(is_valid_user))
    if not is_valid_user:
        return abort(
            HTTPStatus.UNAUTHORIZED, message='User is not registered')


async def handle_users_get(user):
    authenticated = await user_manager.authenticate_user(user,
                                                         app.http_session)
    return HTTPStatus.OK if authenticated else HTTPStatus.UNAUTHORIZED


async def handle_users_post(user):
    registration = await user_manager.register_user(user, app.http_session)
    return HTTPStatus.CREATED if registration else HTTPStatus.CONFLICT

async def check_unvoted_count(unvoted, user):
    if unvoted < content_config['unvoted_threshold']:
        getLogger("root").warn(
            '%s has %d unvoted posts remaining. Requesting content',
            user, unvoted)
        await request_content(content_config)


async def request_content(config):
    data = {'count': config['unvoted_threshold'],
            'return_url': config['self']}
    url = config['url']

    post = app.http_session.post(url, json=data)
    async with post as response:
        await response.text()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
