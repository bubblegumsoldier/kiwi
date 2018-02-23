from os import environ
from collections import namedtuple
from surprise import KNNWithMeans

MySQLConfig = namedtuple('MySQLConfig', 'host port user password db')


def create_algorithm():
    """
    See: http://surprise.readthedocs.io/en/stable/prediction_algorithms.html
    """
    # sim_options = {
    #     'name': 'cosine',
    #     'user_based': False
    # }
    algo = KNNWithMeans(min_k=0, k=40, sim_options={'user_based': False})
    return algo

# _dir_path = path.dirname(os.path.realpath(__file__))

# temp_folder = path.join(_dir_path, ".temp")


def read_mysql_config():
    return MySQLConfig(
        host=environ.get('MSQL_HOST', None),
        port=int(environ.get('MSQL_PORT', 0)),
        user=environ.get('MSQL_USER', None),
        password=environ.get('MSQL_PWD', None),
        db=environ.get('MSQL_DATABASE', None)
    )
