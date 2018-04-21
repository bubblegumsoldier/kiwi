from os import environ
from collections import namedtuple

MySQLConfig = namedtuple('MySQLConfig', 'host port user password db')



def read_mysql_config():
    """
    Reads the environment variables injected by docker/docker-compose/virtualenv to connect to the mysql database.
    """
    return MySQLConfig(
        host=environ.get('MSQL_HOST', None),
        port=int(environ.get('MSQL_PORT', 0)),
        user=environ.get('MSQL_USER', None),
        password=environ.get('MSQL_PWD', None),
        db=environ.get('MSQL_DATABASE', None)
    )

def read_config():
    return {
        "max_rating": float(environ.get('MAX_RATING', 1)),
        "min_rating": float(environ.get('MIN_RATING', 0)),
        "positive_cutoff": float(environ.get('POS_CUTOFF', 0)) # rating > cutoff -> 1, sonst -1
    }
