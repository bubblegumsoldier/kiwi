from sanic.log import error_logger


def log_exception(exceptions=(Exception), reraise=True):
    def decorator(func):
        async def helper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                error_logger.exception('{0!r}'.format(e))
                if reraise:
                    raise e
        return helper
    return decorator
