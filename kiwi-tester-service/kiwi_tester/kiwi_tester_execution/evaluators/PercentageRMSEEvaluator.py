from sklearn.metrics import mean_squared_error
import numpy as np
from math import sqrt, floor, ceil
from functools import partial


class PercentageRMSEEvaluator:
    def __init__(self, decoratee=None):
        self._decoratee = decoratee

    def evaluate(self, matrixA, matrixB):
        matrixA = np.array(matrixA)
        matrixB = np.array(matrixB)
        rmse_slice = partial(sliced_rmse, matrixA, matrixB)
        # for i, el in enumerate(matrixA):
        #     print("{0:.2f}|{1:.2f}".format(el, matrixB[i]))
        if self._decoratee:
            matrixA = self._decoratee.convert(matrixA)
            matrixB = self._decoratee.convert(matrixB)

        percentages = [(rmse_slice(lower, lower + 0.2), lower, lower + 0.2)
                       for lower in np.arange(0.0, 1.0, 0.2)]
        total = (sqrt(mean_squared_error(matrixA, matrixB)), 0, 1)

        return percentages + [total]


def sliced_rmse(matrixA, matrixB, lower_bound, upper_bound):
    item_count = matrixA.shape[0]
    lower = floor(item_count * lower_bound)
    upper = ceil(item_count * upper_bound)
    return sqrt(mean_squared_error(matrixA[lower:upper], matrixB[lower:upper]))
