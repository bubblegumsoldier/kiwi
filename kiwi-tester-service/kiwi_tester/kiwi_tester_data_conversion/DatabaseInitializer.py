class DatabaseInitializer():
    def __init__(self, config):
        self._config = config

    def initialize_database_with(self, data):
        raise NotImplementedError("To be implemented")