#python
import os
import json

#flask
from flask import request

#kiwi
import database_initializer
import Authenticator

#main
if __name__ == "__main__":
    main()

user_database_connection = None

#initializing code
def main():
    user_database_connection = database_initializer.initialize_database()
    app = Flask(__name__)

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
    
    authenticator = Authenticator(username, user_database_connection)
    result = authenticator.authenticate()
    response = {
        'valid': result
    }
    return (json.encode(response), HTTPStatus.ACCEPTED)

@app.route("/register", methods=["POST"])
def register():
    #TODO
    pass