from collections import namedtuple


MongoConfig = namedtuple(
    'MongoConfig', 'host port db collection username password')
Config = namedtuple(
    'Config', 'request_templates forbidden_types reset_page_time')
RequestTemplate = namedtuple('RequestTemplate', 'url tag order window secret')
