from os import environ, path
from collections import namedtuple
from json import load

MySQLConfig = namedtuple('MySQLConfig', 'host port user password db')
AppConfig = namedtuple('AppConfig', 'host port')


def read_mysql_config():
    return MySQLConfig(
        host=environ['MSQL_HOST'],
        port=int(environ['MSQL_PORT']),
        user=environ['MSQL_USER'],
        password=environ['MSQL_PWD'],
        db=environ['MSQL_DATABASE']
    )


def read_rating_config():
    return {
        "min_rating": environ.get('MIN_RATING', 0),
        "max_rating": environ.get('MAX_RATING', 1)
    }


def read_app_config():
    with open(path.join(path.dirname(__file__), 'config.json')) as f:
        config = load(f)
        return AppConfig(**config)
