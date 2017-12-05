from os import path
from collections import namedtuple
from json import load

ConnectionParams = namedtuple('ConnectionParams', 'host port') 

def load_config():
    with open(path.join(path.dirname(__file__), 'config.json')) as f:
        config = load(f)
        return config