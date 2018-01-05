from http import HTTPStatus
from logging import getLogger
from asyncio import ensure_future
from sanic import Sanic
from sanic.response import text
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from kiwi.Collector import Collector
from kiwi.DatabaseConnection import CollectionManipulator
from kiwi.PostExtractor import PostExtractor
from kiwi.config import read_config, read_mongo_config
from kiwi.Sender import Sender
from kiwi.Requester import Requester

app = Sanic(__name__)
requester_config = read_config()


@app.listener('before_server_start')
async def setup(sanic, loop):
    config = read_mongo_config()
    client = AsyncIOMotorClient(host=config.host, port=config.port,
                                username=config.username, password=config.password)
    collection = client[config.db][config.collection]

    sanic.collection_manipulator = CollectionManipulator(collection)
    sanic.db_client = client
    sanic.http_session = ClientSession(loop=loop)


@app.listener('after_server_stop')
async def teardown(sanic, loop):
    await sanic.http_session.close()
    sanic.  db_client.close()


@app.route('/items', methods=['POST'])
async def new_items(request):
    '''
    Parses the request, expexts a json object of form {count, return_url}.
    Returns no content, but will make a request to the given url, once enough
    new content has been requested.
    '''
    post_data = request.json
    if validate_post_data(post_data):
        getLogger("root").info('received request {!r}'.format(post_data))
        sender = Sender(app.http_session,
                        post_data['return_url'],
                        app.collection_manipulator)
        collector = Collector(post_data['count'],
                              build_requesters(),
                              sender.store_posts_and_send)
        ensure_future(collector.run_requests())
        return text('Accepted', HTTPStatus.ACCEPTED)
    return text('Post data invalid', HTTPStatus.BAD_REQUEST)


def build_requesters():
    post_extractor = PostExtractor(
        requester_config.forbidden_types, app.collection_manipulator.post_exists)
    requesters = [Requester(session=app.http_session,
                            url_template=requester_config.url,
                            path=topic,
                            extraction_function=post_extractor.
                            extract_and_filter_duplicates)
                  for topic in requester_config.topics]
    return requesters

def validate_post_data(post_data):
    return post_data.get('return_url') and post_data.get('count') >= 0


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)