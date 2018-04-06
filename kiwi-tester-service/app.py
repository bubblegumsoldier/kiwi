from kiwi_tester.KiwiTester import KiwiTester
from kiwi_tester.KiwiTesterConfig import KiwiTesterConfig

#from kiwi_tester.kiwi_tester_data_conversion.converter.MatrixConverter import MatrixConverter
#from kiwi_tester.kiwi_tester_data_conversion.converter.FlatMatrixConverter import FlatMatrixConverter
#from kiwi_tester.kiwi_tester_data_conversion.converter.NoneContainingMatrixConverter import NoneContainingMatrixConverter
from kiwi_tester.kiwi_tester_data_conversion.data_splitter.ListUserPercentageSplitter import ListUserPercentageSplitter
from kiwi_tester.kiwi_tester_data_conversion.product_converter.DefaultProductConverter import DefaultProductConverter

config = KiwiTesterConfig(
    data_converter = ListUserPercentageSplitter(0.8
        #NoneContainingMatrixConverter(
        #    FlatMatrixConverter()
        #)
    ),
    product_converter = DefaultProductConverter(),
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

products = [
    ("product_1", ["tag1", "tag2", "tag3"]),
    ("product_2", ["tag1", "tag2", "tag3"]),
    ("product_3", ["tag1", "tag2", "tag3"]),
    ("product_4", ["tag1", "tag2", "tag3"]),
    ("product_5", ["tag1", "tag2", "tag3"]),
    ("product_6", ["tag1", "tag2", "tag3"]),
    ("product_7", ["tag1", "tag2", "tag3"]),
    ("product_8", ["tag1", "tag2", "tag3"]),
    ("product_9", ["tag1", "tag2", "tag3"]),
    ("product_10", ["tag1", "tag2", "tag3"]),
    ("product_11", ["tag1", "tag2", "tag3"]),
    ("product_12", ["tag1", "tag2", "tag3"])
]

tester = KiwiTester(data, products, config)
tester.start_full_procedure()