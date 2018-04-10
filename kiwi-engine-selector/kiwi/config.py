from os import path, environ
from json import load
from ast import literal_eval

with open(path.join(path.dirname(__file__), 'config.json')) as file:
    CONFIG = load(file)

def read_recommenders():
    """
    store recommenders as name=address;name=
    """
    var = literal_eval(environ.get('RECOMMENDERS', 'None'))
    if var:
        return dict(recomm.strip().split('=') for recomm in var)
    return {}




RECOMMENDERS = read_recommenders()
APP_CONFIG = CONFIG['app']
HEURISICS_CONFIG = CONFIG['heuristics']