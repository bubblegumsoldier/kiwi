class ListUserPercentageSplitter:
    def __init__(self, training_percentage, decoratee = None):
        self._training_percentage = training_percentage
        self._decoratee = decoratee
    
    def convert(self, dataset):
        """
        dataset is array of tuple with content (user, item, vote)...

        [
            (user, item, vote),
            ...
        ]

        and it will return a tuple containing two arrays of the same structure
        (testing and training)
        """
        if self._decoratee is not None:
            dataset = self._decoratee.convert(dataset)
            print("ListUserPercentageSplitter received dataset looking like: \n")
            import json
            print(json.dumps(dataset, indent=4, sort_keys=True))
        print("Converting with ListUserPercentageSplitter")
        return self._split_into_two_sets(dataset)

    def _split_into_two_sets(self, dataset):
        training_set = []
        testing_set = []
        
        for l in dataset:
            username = l[0]
            next_reached_training_ratio = float(self._get_number_of_votes_for_user_in_dataset(username, training_set) + 1) / float(self._get_number_of_votes_for_user_in_dataset(username, dataset))
            if next_reached_training_ratio > self._training_percentage:
                testing_set.append(l)
            else:
                training_set.append(l)

        print("Splitted Dataset into {} training and {} testing elements".format(len(training_set), len(testing_set)))

        return training_set, testing_set

    def _get_number_of_votes_for_user_in_dataset(self, user, dataset):
        votes_of_user = [True for u in dataset if u[0] == user]
        return len(votes_of_user)

    def __getattr__(self, name):
        return getattr(self._decoratee, name)