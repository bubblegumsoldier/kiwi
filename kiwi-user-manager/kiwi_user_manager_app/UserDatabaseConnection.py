import mysql.connector

class UserDatabaseConnection(object):
    _user_table = "users"

    def __init__(self, connection_details):
        self.connection_details = connection_details
    
    def establish(self):
        c_connection = mysql.connector.connect(**self.connection_details)
        except mysql.connector.Error as err:
            self._connection = None
            return err
        else:
            self._connection = c_connection
            return True
    
    def has_connection(self):
        return self._connection is not None
    
    def has_username(self, username):
        query = ("SELECT id FROM %s WHERE username = %s")
        
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, (UserDatabaseConnection._user_table, username))
            return cursor.rowcount > 0
        except:
            return False #TODO: Exception handling