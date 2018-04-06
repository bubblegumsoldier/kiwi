class NoneContainingMatrixConverter:
    def __init__(self, decoratee = None):
        self._decoratee = decoratee
    
    def convert(self, dataset):
        """
        Takes a matrix of user x products containing ratings and replaces all
        None values with the mean value of ratings for the user
        """
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
            print("NoneContainingMatrixConverter received dataset looking like: \n")
            import json
            print(json.dumps(dataset, indent=4, sort_keys=True))
        print("Converting with NoneContainingMatrixConverter")
        
        for user_id, ratings in enumerate(dataset):
            ratings_list_without_none = [float(rating) for rating in ratings if rating is not None]
            mean = sum(ratings_list_without_none) / len(ratings_list_without_none)
            new_ratings = [mean if v is None else v for v in ratings]
            dataset[user_id] = new_ratings

        return dataset

    def __getattr__(self, name):
        return getattr(self._decoratee, name)