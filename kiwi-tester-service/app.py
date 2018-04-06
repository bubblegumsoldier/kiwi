from kiwi_tester.KiwiTester import KiwiTester
from kiwi_tester.KiwiTesterConfig import KiwiTesterConfig

#from kiwi_tester.kiwi_tester_data_conversion.converter.MatrixConverter import MatrixConverter
#from kiwi_tester.kiwi_tester_data_conversion.converter.FlatMatrixConverter import FlatMatrixConverter
#from kiwi_tester.kiwi_tester_data_conversion.converter.NoneContainingMatrixConverter import NoneContainingMatrixConverter
from kiwi_tester.kiwi_tester_data_conversion.data_splitter.ListUserPercentageSplitter import ListUserPercentageSplitter

config = KiwiTesterConfig(
    data_converter = ListUserPercentageSplitter(0.8
        #NoneContainingMatrixConverter(
        #    FlatMatrixConverter()
        #)
    ),
    testing_style = "instantfeedback",
    mysql_config = {
        'host': '...',
        'username': '...',
        'pw': '...',
        'database': '...',
        'table_prefix': '...'
    },
    service_domain = "http://.../"
)

data = [
    ("bubblegumsoldier", "product_1", 1),
    ("bubblegumsoldier", "product_2", 0),
    ("bubblegumsoldier", "product_4", 1),
    ("bubblegumsoldier", "product_5", 1),
    ("bubblegumsoldier", "product_8", 1),
    ("bubblegumsoldier", "product_9", 1),
    ("bubblegumsoldier", "product_10", 1),
    ("bubblegumsoldier", "product_12", 1),
    ("peter", "product_1", 1),
    ("peter", "product_2", 0),
    ("peter", "product_3", 0),
    ("peter", "product_8", 0),
    ("peter", "product_12", 0)
]

tester = KiwiTester(data, config)
tester.start_full_procedure()