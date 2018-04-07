class ListMatrixColumnRemover:
    def __init__(self, column_id, decoratee = None):
        self.column_id = column_id
        self._decoratee = decoratee
    
    def convert(self, dataset):
        """
        Receives a dataset like this
        [
            (item_0, item_1, item_2, ...)
        ]
        and uses the initialized column id to remove the column
        e.g. column_id = 1
        [
            (item_0, item_2, item_3, ...)
        ]
        """
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
        
        new_list = [self._convert_item(t) for t in dataset]

        return new_list

    def _convert_item(self, t):
        as_list = list(t)
        del as_list[self.column_id]
        return tuple(as_list)

    def __getattr__(self, name):
        return getattr(self._decoratee, name)