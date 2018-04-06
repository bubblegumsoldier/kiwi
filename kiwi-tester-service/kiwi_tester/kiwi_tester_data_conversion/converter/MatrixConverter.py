class MatrixConverter:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def convert(self, dataset):
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
            print("MatrixConverter received dataset looking like: \n")
            import json
            print(json.dumps(dataset, indent=4, sort_keys=True))
        print("Converting with MatrixConverter")
        #potential place to do conversion
        return dataset

    def __getattr__(self, name):
        return getattr(self._decoratee, name)