#python
import json
from http import HTTPStatus
from flask_cors import CORS
#flask
from flask import (Flask, request, jsonify)

#initializing code
app = Flask(__name__)
CORS(app)

#kiwi
from lib.Authenticator import Authenticator
from lib.RegisterService import RegisterService
from lib.database_initializer import initialize_database

@app.route("/authenticate/<username>", methods=['GET', 'POST'])
def authenticate(username):
    """
    Authentication endpoint (/authenticate).

    The request parameter "username" will be needed.

    A JSON response will be returned containing a dict with the attribute "valid" (true/false).
    """
    if not username:
        return ('Post data invalid', HTTPStatus.BAD_REQUEST)
    
    authenticator = Authenticator(initialize_database())
    result = authenticator.authenticate(username)
    response = {
        'valid': result
    }
    return jsonify(response)

@app.route("/register/<username>", methods=["POST", "GET"])
def register(username):
    """
    Registration Endpoint (/register).

    The request parameter "username" will be needed.

    A JSON response will be returned containing a dict with the attribute "success" (true/false).
    """
    if not username:
        return ('Post data invalid', HTTPStatus.BAD_REQUEST)

    register_service = RegisterService(initialize_database())
    result = register_service.register(username)
    response = {
        "success": result
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()