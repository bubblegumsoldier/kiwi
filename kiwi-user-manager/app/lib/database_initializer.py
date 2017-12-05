#python
import os

#kiwi
from lib.UserDatabaseConnection import UserDatabaseConnection

def initialize_database(connection_details = None):
    if connection_details is None:
        connection_details = {
            'host':     os.environ.get("KIWI_USER_MANAGER_DB_HOST"),
            'user':     os.environ.get("KIWI_USER_MANAGER_DB_USER"),
            'password': os.environ.get("KIWI_USER_MANAGER_DB_PASSWORD"),
            'database': os.environ.get("KIWI_USER_MANAGER_DB_DATABASE")
        }
        print(connection_details)
    connection = UserDatabaseConnection(connection_details)
    print("establishing")
    connection.establish()
    return connection