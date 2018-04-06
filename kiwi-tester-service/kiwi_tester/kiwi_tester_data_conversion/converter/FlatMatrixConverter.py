class FlatMatrixConverter:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def convert(self, dataset):
        """
        dataset is array of tuple with content (user, item, vote)...
        convert will convert it to array of type
        [[vote, vote, vote], [vote, vote, vote], ...]
        where each row is for a user and each vote in it for the item with the index id.
        If no vote for the given index id was found then the average vote value of the user will be put in.
        """
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
        
        print("converting dataset using the FlatMatrixConverter")

        converted_1 = {}
        self._create_product_id_tuple(dataset)

        for t in dataset:
            user = t[0]
            if user not in converted_1:
                converted_1[user] = [None] * self._get_next_product_index()
            converted_1[user][self._get_internal_product_id_for_external(t[1])] = t[2]

        converted_final = [converted_1[k] for k in sorted(converted_1, key=converted_1.get)]

        return converted_final

    def _create_product_id_tuple(self, dataset):
        self.product_to_index_map = {}
        
        for t in dataset:
            external_product_id = t[1]
            if not external_product_id in self.product_to_index_map:
                self.product_to_index_map[external_product_id] = self._get_next_product_index()
            
    def _get_internal_product_id_for_external(self, external_product_id):
        return self.product_to_index_map[external_product_id]
    
    def _get_next_product_index(self):
        if not self.product_to_index_map:
            return 0
        import operator
        return max(self.product_to_index_map.iteritems(), key=operator.itemgetter(1))[1] + 1


    def __getattr__(self, name):
        return getattr(self._decoratee, name)