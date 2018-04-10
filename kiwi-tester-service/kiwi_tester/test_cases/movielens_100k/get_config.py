from kiwi_tester.KiwiTesterConfig import KiwiTesterConfig
from kiwi_tester.kiwi_tester_data_conversion.data_splitter.RandomPercentageSplitter import RandomPercentageSplitter
from kiwi_tester.kiwi_tester_data_conversion.product_converter.DefaultProductConverter import DefaultProductConverter
from kiwi_tester.kiwi_tester_data_conversion.converter.EasyMatrixNormalizer import EasyMatrixNormalizer
from kiwi_tester.kiwi_tester_execution.evaluators.RMSEEvaluator import RMSEEvaluator

def get_config():
    config = KiwiTesterConfig(
        data_converter = RandomPercentageSplitter(0.8),
        product_converter = DefaultProductConverter(),
        service_domain = "http://google.de/",
        evaluator = RMSEEvaluator(EasyMatrixNormalizer(4))
    )
    return config