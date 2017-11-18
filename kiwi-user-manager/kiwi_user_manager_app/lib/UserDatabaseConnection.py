from pymongo import MongoClient

class UserDatabaseConnection(object):
    _user_table = "users"

    def __init__(self, connection_details):
        """
        The constructor to store the connection to the database.

        To establish a connection call the establish() method.

        connection_details -- A dict containing an entry for user, password, host and database.
        """
        self.connection_details = connection_details
    
    def establish(self):
        """
        Establishes a connection to the database server (MongoDB).
        """
        username = self.connection_details.get("user")
        password = self.connection_details.get("password")
        host = self.connection_details.get("host")
        database = self.connection_details.get("database")
        try:
            c_client = MongoClient('mongodb://%s:%s@%s' % (username, password, host))
            c_db = c_client[database]
        except Exception as e:
            print(e)
            self._client = None
            self.db = None
            return False
        else:
            self._client = c_client
            self._db = c_db
            return True

    def has_connection(self):
        v = hasattr(self, "_client") and self._client is not None
        return v
    
    def has_username(self, username):
        return self._db[self._user_table].find_one({"username": username}) is not None

    def insert(self, username):
        # I have no idea of mongodb and don't know if there is something like a mysql-unique equivalent.
        # Cause this should not be the place to check for doubles
        # TODO
        
        if self.has_username(username):
            return False

        self._db[self._user_table].insert_one({"username": username})
        return True