from kiwi_tester.kiwi_tester_database_access.DatabaseAccessor import DatabaseAccessor

class DatabaseInitializer():
    def __init__(self, config):
        self._config = config

    def initialize_database_with(self, training_data, testing_data):
        print("Initializing testing database...")
        self._database_accessor = DatabaseAccessor(self._config)
        self._append_prediction_column_to_testing_set(testing_data)
        self._database_accessor.initialize_database(training_data, testing_data)
        print("--> Successfully initialized testing database")

    def _append_prediction_column_to_testing_set(self, testing_data):
        return [(v[0], v[1], v[2], None) for v in testing_data]