from sklearn.metrics import mean_squared_error
from math import sqrt

class RMSEEvaluator:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def evaluate(self, matrixA, matrixB):
        for i, el in enumerate(matrixA):
            print("{0:.2f}|{1:.2f}".format(el, matrixB[i]))
        if self._decoratee:
            matrixA = self._decoratee.convert(matrixA)
            matrixB = self._decoratee.convert(matrixB)
        
        return sqrt(mean_squared_error(matrixA, matrixB))