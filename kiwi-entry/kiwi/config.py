from os import path, environ
from collections import namedtuple
from json import load


ConnectionParams = namedtuple('ConnectionParams', 'host port') 

def load_config():
    return {
        'user_service': environ.get('USER_SERVICE', ""),
        'switcher_service': environ.get('SWITCHER_SERVICE', "")
    }


def get_content_config():
    return {
        'unvoted_threshold': int(environ.get('UNVOTED_THRESHOLD', 50)),
        'url': environ.get('CONTENT_SERVICE'),
        'self': environ.get('SELF') # url
    }
