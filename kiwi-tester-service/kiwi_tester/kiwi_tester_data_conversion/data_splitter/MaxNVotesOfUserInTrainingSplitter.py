import sys
class MaxNVotesOfUserInTrainingSplitter:
    def __init__(self, n, decoratee = None):
        self._n = n
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
            print("MaxNVotesInTrainingSplitter received dataset looking like: \n")
            import json
            print(json.dumps(dataset, indent=4, sort_keys=True))
        print("Converting with MaxNVotesInTrainingSplitter")
        two_sets = self._split_into_two_sets(dataset)        
        return two_sets

    def _split_into_two_sets(self, dataset):
        training_set = []
        testing_set = []

        for el in dataset:
            if self._n == 0:
                # a little performance tweak
                testing_set.append(el)
                continue

            if self._get_votes_of_user_in_training_set(training_set, el[0]) <= self._n:
                training_set.append(el)
            else:
                testing_set.append(el)

        print("Splitted Dataset into {} training and {} testing elements".format(len(training_set), len(testing_set)))

        return training_set, testing_set

    def _get_votes_of_user_in_training_set(self, training_set, user):
        return len([True for el in training_set if el[0] == user])

    def __getattr__(self, name):
        return getattr(self._decoratee, name)