from http import HTTPStatus
from pymysql.err import OperationalError, IntegrityError, ProgrammingError
from sanic.response import json


def return_exception_as_json(exceptions=(Exception)):    
    def decorator(func):
        async def helper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                return json({"error": e.args},
                            map_exception_to_http_code(e))
        return helper
    return decorator


def map_exception_to_http_code(exception=(Exception)):
    if isinstance(exception, (OperationalError, ProgrammingError)):
        return HTTPStatus.INTERNAL_SERVER_ERROR
    if isinstance(exception, (IntegrityError)):
        return HTTPStatus.BAD_REQUEST
    return HTTPStatus.BAD_GATEWAY
