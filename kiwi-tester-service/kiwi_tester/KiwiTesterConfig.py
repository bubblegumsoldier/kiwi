from kiwi_tester.kiwi_tester_data_conversion.converter.MatrixConverter import MatrixConverter
from kiwi_tester.kiwi_tester_data_conversion.product_converter.DefaultProductConverter import DefaultProductConverter
from kiwi_tester.kiwi_tester_execution.evaluators.RMSEEvaluator import RMSEEvaluator

class KiwiTesterConfig:
    def __init__(self, **kwargs):
        self._init_defaults()
        self.data_converter = kwargs.get("data_converter")
        self.product_converter = kwargs.get("product_converter")
        self.testing_style = kwargs.get('testing_style')
        self.mysql_config = kwargs.get('mysql_config')
        self.service_domain = kwargs.get('service_domain')
        self.evaluator = kwargs.get("evaluator")
        self.skip_products = kwargs.get("skip_products")
        self.skip_training = kwargs.get("skip_training")
        self.skip_testing = kwargs.get("skip_testing")

    def _init_defaults(self):
        self.data_converter = MatrixConverter()
        self.product_converter = DefaultProductConverter()
        self.testing_style = 'instant'
        self.mysql_config = {
            'host': '...',
            'username': '...',
            'pw': '...',
            'database': '...',
            'table_prefix': '...'
        }
        self.service_domain = '...'
        self.evaluator = RMSEEvaluator()
        self.skip_products = False
        self.skip_training = False
        self.skip_testing = False