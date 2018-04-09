class EasyMatrixNormalizer:
    def __init__(self, factor, decoratee = None):
        self._decoratee = decoratee
        self.factor = factor
    
    def convert(self, dataset):
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
        for i, a in enumerate(dataset):
            dataset[i] = float(a) / float(self.factor)
        return dataset

    def __getattr__(self, name):
        return getattr(self._decoratee, name)