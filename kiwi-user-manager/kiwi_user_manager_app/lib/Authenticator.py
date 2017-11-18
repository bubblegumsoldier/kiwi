class Authenticator(object):
    def __init__(self, user_database_connection):
        """
        Should be used to create an Authenticator object.
        The Authenticator class should be used to check whether given credentials are 
        valid and stored within the database.

        user_database_connection -- object of type UserDatabaseConnection that
                                    wraps the database connection
        """
        self.user_database_connection = user_database_connection
    
    def authenticate(self, username):
        """
        This is the main authentication method. It checks whether a user with given credentials exists in the database.
        
        username -- string of the username that should be checked

        Returns False if non-existant and True if existant
        """
        if not self.user_database_connection or not self.user_database_connection.has_connection():
            #TODO: Add exception or something
            return False
        search_result = self.user_database_connection.has_username(username)
        return False if not search_result else True