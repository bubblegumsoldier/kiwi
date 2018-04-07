from sklearn.metrics import mean_squared_error

class RMSEEvaluator:
    def __init__(self):
        pass
    
    def evaluate(self, matrixA, matrixB):
        return mean_squared_error(matrixA, matrixB)