from os import environ, path
from collections import namedtuple
from ast import literal_eval
import importlib
  

MySQLConfig = namedtuple('MySQLConfig', 'host port user password db')


def get_algorithm_config():
    """
    ALGO_PATH needs to be an environment variable that stores a relative
    path, from the directory of this file to the file that contains the 
    algorithm configuration.
    """
    base_path = path.dirname(path.realpath(__file__))
    rel_path = environ.get('ALGO_PATH', 'algorithms/knn_user.py')
    spec = importlib.util.spec_from_file_location("algorithm", path.join(base_path, rel_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

get_algorithm_config()


def read_rating_config():
    return (
        float(environ.get('MIN_RATING', 0)),
        float(environ.get('MAX_RATING', 1)),
    )


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


def set_retraining_cycle():
    """
    Setting RETRAINING_TIME retrains the algorithm periodically (seconds)
    Setting ON_REQUEST retrains it after a request to the given endpoint(s)
    """
    periodic = environ.get('RETRAINING_TIME')
    on_request = literal_eval(environ.get('RETRAIN_ON_REQUEST', '[]'))
    return {
        'on_request': on_request,
        'periodic': int(periodic) if periodic else periodic
    }
