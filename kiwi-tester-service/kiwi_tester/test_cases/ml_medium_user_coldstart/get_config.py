from kiwi_tester.KiwiTesterConfig import KiwiTesterConfig
from kiwi_tester.kiwi_tester_data_conversion.data_splitter.TopNUsersInTestingSplitter import TopNUsersInTestingSplitter
from kiwi_tester.kiwi_tester_data_conversion.product_converter.DefaultProductConverter import DefaultProductConverter
from kiwi_tester.kiwi_tester_data_conversion.converter.EasyMatrixNormalizer import EasyMatrixNormalizer
from kiwi_tester.kiwi_tester_execution.evaluators.RMSEEvaluator import RMSEEvaluator
from datetime import datetime


def get_config():
    now_as_string = str(datetime.now()).replace(" ", "_").replace(":", "_").replace("-", "_").replace(".", "_")
    config = KiwiTesterConfig(
        data_converter = TopNUsersInTestingSplitter(1),
        product_converter = DefaultProductConverter(),
        service_domain = "http://localhost:8000/",
        evaluator = RMSEEvaluator(EasyMatrixNormalizer(1)),
        stats_output = "/stats/movielens_very_small_stats_{}.txt".format(now_as_string)
    )
    return config