from lib.username_validator import validate
from werkzeug.exceptions import abort
from http import HTTPStatus

class RegisterService(object):
    def __init__(self, user_database_connection):
        """
        A class that should be used to register a new user.

        user_database_connection -- object of type UserDatabaseConnection that
                                    wraps the database connection
        """
        self.user_database_connection = user_database_connection

    def register(self, username):
        if not validate(username):
            abort(HTTPStatus.NOT_ACCEPTABLE)
            
        return self.user_database_connection.insert(username)