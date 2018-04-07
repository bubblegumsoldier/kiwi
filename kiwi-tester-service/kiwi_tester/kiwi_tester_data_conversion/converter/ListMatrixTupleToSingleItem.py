class ListMatrixTupleToSingleItem:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def convert(self, dataset):
        """
        Receives a dataset like this
        [
            (item_0),
            (item_1)
        ]
        and converts it to 
        [
            item_0,
            item_1
        ]
        """
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
                
        new_list = [a[0] for a in dataset]

        return new_list

    def __getattr__(self, name):
        return getattr(self._decoratee, name)