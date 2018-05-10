from kiwi_tester.kiwi_tester_database_access.DatabaseAccessor import DatabaseAccessor

from kiwi_tester.kiwi_tester_data_conversion.converter.ListMatrixColumnRemover import ListMatrixColumnRemover
from kiwi_tester.kiwi_tester_data_conversion.converter.ListMatrixTupleToSingleItem import ListMatrixTupleToSingleItem

class KiwiEvaluator:
    def __init__(self, config, statistic_container):
        self._config = config
        self.statistic_container = statistic_container

    def get_evaluation(self):
        dba = DatabaseAccessor(self._config)
        original_testing_matrix = []
        dba.go_to_first_testing()
        while dba.has_next_testing():
            c_testing = dba.get_next_testing()
            original_testing_matrix.append(c_testing)

        remover_to_create_prediction_m = ListMatrixTupleToSingleItem(ListMatrixColumnRemover(0, ListMatrixColumnRemover(0, ListMatrixColumnRemover(1))))
        remover_to_create_original_m = ListMatrixTupleToSingleItem(ListMatrixColumnRemover(1, ListMatrixColumnRemover(0, ListMatrixColumnRemover(0))))

        prediction_matrix = remover_to_create_prediction_m.convert(original_testing_matrix)
        original_matrix = remover_to_create_original_m.convert(original_testing_matrix)

        evaluation = self._config.evaluator.evaluate(original_matrix,prediction_matrix)
        self.statistic_container.set_evaluation_score(evaluation)
        self.statistic_container.counts_of_single_recommenders()
        return evaluation