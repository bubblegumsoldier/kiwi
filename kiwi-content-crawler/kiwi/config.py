from os import path, environ
from json import load

from kiwi.Types import RequestTemplate, Config, MongoConfig


def read_config():
    with open(path.join(path.dirname(__file__), 'config.json')) as file:
        config = load(file)
        request_templates = [
            RequestTemplate(
                **topic,
                url=config['url'],
                secret=environ.get('IMGUR_CLIENT_ID'))
            for topic in config['topics']]

        return Config(request_templates=request_templates,
                      forbidden_types=config['forbidden_types'],
                      reset_page_time=int(environ.get('RESET_PAGE_TIME')))


def read_mongo_config():
    host = environ.get('MONGO_HOST')
    port = int(environ.get('MONGO_PORT'))
    db = environ.get('MONGO_DB')
    collection = environ.get('MONGO_COLLECTION')
    user = environ.get('MONGO_USER')
    pwd = environ.get('MONGO_PWD')

    return MongoConfig(host=host,
                       port=port,
                       db=db,
                       collection=collection,
                       username=user,
                       password=pwd)
