from os import path
from json import load

with open(path.join(path.dirname(__file__), 'config.json')) as file:
    CONFIG = load(file)


RECOMMENDERS = CONFIG['recommenders']
APP_CONFIG = CONFIG['app']
HEURISICS_CONFIG = CONFIG['heuristics']