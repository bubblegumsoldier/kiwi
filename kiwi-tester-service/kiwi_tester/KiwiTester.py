from kiwi_tester.KiwiTesterConfig import KiwiTesterConfig 

from kiwi_tester.kiwi_tester_data_conversion.DatabaseInitializer import DatabaseInitializer

from kiwi_tester.kiwi_tester_execution.KiwiContentInitializer import KiwiContentInitializer

class KiwiTester:
    
    def __init__(self, data, products, config = KiwiTesterConfig()):
        self.raw_data = data
        self.raw_products = products
        self.config = config
    
    def start_full_procedure(self):
        self.convert_data_and_initialize_database()
        self.do_training_and_testing()
    
    def do_training_and_testing(self):
        self.do_training()
        self.do_testing()

    def do_training(self):
        self.initialize_content()
        self.simulate_training()

    def simulate_training(self):
        pass

    def initialize_content(self):
        self.convert_content()
        self.content_initializer = KiwiContentInitializer(self.config)
        self.content_initializer.initialize_products(self.products)

    def convert_content(self):
        self.products = [self.config.product_converter.convert(product) for product in self.raw_products]
    
    def do_testing(self):
        pass

    def convert_data_and_initialize_database(self):
        self.convert_data()
        self.initialize_database_with_converted_data()

    def convert_data(self):
        self.converter = self.config.data_converter
        self.training_data, self.testing_data = self.converter.convert(self.raw_data)

    def initialize_database_with_converted_data(self):
        self.database_initializer = DatabaseInitializer(self.config)
        self.database_initializer.initialize_database_with(self.training_data, self.testing_data)