class ServerError(Exception):
    def __init__(self, message, error_code):

        # Call the base class constructor with the parameters it needs
        super(ServerError, self).__init__("{} - ({})".format(message, error_code))

        # Now for your custom code...
        self.error_code = error_code