from os import path, environ
from collections import namedtuple
from json import load

Topic = namedtuple('Topic', 'tag order window')
MongoConfig = namedtuple(
    'MongoConfig', 'host port db collection username password')
Config = namedtuple('Config', 'url topics forbidden_types')


def read_config():
    with open(path.join(path.dirname(__file__), 'config.json')) as file:
        config = load(file)
        topics = [Topic(**topic) for topic in config['topics']]
        
        return Config(url=config['url'],
                      topics=topics,
                      forbidden_types=config['forbidden_types'])


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
