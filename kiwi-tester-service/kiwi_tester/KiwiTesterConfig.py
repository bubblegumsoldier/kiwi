from kiwi_tester.kiwi_tester_data_conversion.converter.MatrixConverter import MatrixConverter
from kiwi_tester.kiwi_tester_data_conversion.product_converter.DefaultProductConverter import DefaultProductConverter

class KiwiTesterConfig:
    def __init__(self, **kwargs):
        self._init_defaults()
        self.data_converter = kwargs.get("data_converter")
        self.product_converter = kwargs.get("product_converter")
        self.testing_style = kwargs.get('testing_style')
        self.mysql_config = kwargs.get('mysql_config')
        self.service_domain = kwargs.get('service_domain')

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