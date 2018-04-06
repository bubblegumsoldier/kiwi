from kiwi_tester.KiwiTesterConfig import KiwiTesterConfig 

from kiwi_tester.kiwi_tester_data_conversion.DatabaseInitializer import DatabaseInitializer

class KiwiTester:
    
    def __init__(self, data, config = KiwiTesterConfig()):
        self.raw_data = data
        self.config = config
    
    def start_full_procedure(self):
        self.convert_data_and_initialize_database()


    def convert_data_and_initialize_database(self):
        self.convert_data()
        self.initialize_database_with_converted_data()

    def convert_data(self):
        self.converter = self.config.data_converter
        self.training_data, self.testing_data = self.converter.convert(self.raw_data)

    def initialize_database_with_converted_data(self):
        self.database_initializer = DatabaseInitializer(self.config)
        self.database_initializer.initialize_database_with(self.training_data, self.testing_data)