from os import environ
from collections import namedtuple
import surprise

MySQLConfig = namedtuple('MySQLConfig', 'host port user password db')


def create_algorithm():
    """
    See: http://surprise.readthedocs.io/en/stable/prediction_algorithms.html
    Just change the algorithm and the option set for a different prediction algorithm.
    """
    options = {
        'name': 'cosine',
        'user_based': True
    }
    algo = surprise.KNNWithMeans(
        min_k=1,
        k=40,
        sim_options=options)

    return algo


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
