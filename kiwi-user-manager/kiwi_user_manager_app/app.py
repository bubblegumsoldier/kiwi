#python
import json
from http import HTTPStatus

#flask
from flask import (Flask, request)

#initializing code
app = Flask(__name__)


#kiwi
from lib.Authenticator import Authenticator
from lib.RegisterService import RegisterService
from lib.database_initializer import initialize_database


user_database_connection = initialize_database()

@app.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
    """
    Authentication endpoint (/authenticate).

    The request parameter "username" will be needed.

    A JSON response will be returned containing a dict with the attribute "valid" (true/false).
    """
    username = request.values.get("username")
    if not username:
        return ('Post data invalid', HTTPStatus.BAD_REQUEST)
    
    authenticator = Authenticator(user_database_connection)
    result = authenticator.authenticate(username)
    response = {
        'valid': result
    }
    return (json.dumps(response), HTTPStatus.ACCEPTED)

@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Registration Endpoint (/register).

    The request parameter "username" will be needed.

    A JSON response will be returned containing a dict with the attribute "success" (true/false).
    """
    username = request.values.get("username")
    if not username:
        return ('Post data invalid', HTTPStatus.BAD_REQUEST)

    register_service = RegisterService(user_database_connection)
    result = register_service.register(username)
    response = {
        "success": result
    }

    return (json.dumps(response), HTTPStatus.ACCEPTED)

app.run()