from sklearn.metrics import mean_squared_error

class RMSEEvaluator:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def evaluate(self, matrixA, matrixB):
        if self._decoratee:
            matrixA = self._decoratee.convert(matrixA)
            matrixB = self._decoratee.convert(matrixB)
        
        return mean_squared_error(matrixA, matrixB)