from sanic.config import LOGGING
import logging

# config
HANDLER = 'logging.FileHandler'
FORMATTER = '%(asctime)s - %(levelname)s: %(message)s'
LOGGER = logging.getLogger('kiwi_logger')


def setup_logging():
    LOGGING["formatters"]['my_formatter'] = {
        'format': FORMATTER,
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }

    LOGGING['handlers']['my_handler'] = {
        'class': HANDLER,
        'formatter': 'my_formatter',
        'filename': 'log.log'
    }

    LOGGING["loggers"]['kiwi_logger'] = {
        'level': 'ERROR',
        'handlers': ['my_handler'],
    }


def log_exception(exceptions=(Exception), reraise=True):
    def decorator(func):
        async def helper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                LOGGER.exception('{0!r}'.format(e))
                if reraise:
                    raise e
        return helper
    return decorator
