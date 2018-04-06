from kiwi_tester.kiwi_tester_data_conversion.converter.MatrixConverter import MatrixConverter

class KiwiTesterConfig:
    def __init__(self, **kwargs):
        self._init_defaults()
        self.data_converter = kwargs.get("data_converter")
        self.testing_style = kwargs.get('testing_style')
        self.mysql_config = kwargs.get('mysql_config')
        self.service_domain = kwargs.get('service_domain')

    def _init_defaults(self):
        self.data_converter = MatrixConverter()
        self.testingstyle = 'instantfeedback'
        self.mysql_config = {
            'host': '...',
            'username': '...',
            'pw': '...',
            'database': '...',
            'table_prefix': '...'
        }
        self.service_domain = '...'