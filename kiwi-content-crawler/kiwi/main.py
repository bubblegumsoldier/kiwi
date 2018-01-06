from http import HTTPStatus
from logging import getLogger
from asyncio import ensure_future, sleep
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


async def clear_max_page_after_time():
    while True:
        await sleep(app.app_config.reset_page_time)
        app.current_max_page = 1


@app.listener('before_server_start')
async def setup(sanic: Sanic, loop):
    app_config = read_config()
    mongo_config = read_mongo_config()
    client = AsyncIOMotorClient(host=mongo_config.host,
                                port=mongo_config.port,
                                username=mongo_config.username,
                                password=mongo_config.password)
    collection = client[mongo_config.db][mongo_config.collection]

    sanic.collection_manipulator = CollectionManipulator(collection)
    sanic.db_client = client
    sanic.http_session = ClientSession(loop=loop)
    sanic.app_config = app_config
    sanic.current_max_page = 1
    sanic.processing = False


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
        ensure_future(run_requests(sender, post_data['count']))
        return text('Accepted', HTTPStatus.ACCEPTED)
    return text('Post data invalid', HTTPStatus.BAD_REQUEST)


async def run_requests(sender, count):
    if not app.processing:
        app.processing = True
        try:
            collector = Collector(count,
                                  build_requesters(app))
            posts, max_page = await collector.run_requests()
            await sender.store_posts_and_send(posts)
            app.current_max_page = max_page
        except Exception as exp:
            getLogger('root').error(exp)
        finally:
            app.processing = False
            return
    await sleep(30)
    await run_requests(sender, count)


def build_requesters(sanic):
    post_extractor = PostExtractor(
        sanic.app_config.forbidden_types,
        sanic.collection_manipulator.post_exists)
    requesters = [Requester(session=sanic.http_session,
                            template=template,                    extraction_function=post_extractor.
                            extract_and_filter_duplicates,
                            start_page=app.current_max_page)
                  for template in sanic.app_config.request_templates]
    return requesters


def validate_post_data(post_data):
    return post_data.get('return_url') and post_data.get('count') >= 0


if __name__ == '__main__':
    app.add_task(clear_max_page_after_time)
    app.run(host="0.0.0.0", port=5000)
