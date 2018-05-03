import sys
from numpy.random import shuffle


class MaxNVotesOfUserInTestingMInTraining:
    def __init__(self, n, m, decoratee=None):
        self._n = n
        self._m = m
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
        shuffle(dataset)
        for el in dataset:
            if (self._get_votes_of_user_in_set(testing_set, el[0])
                    < self._n):
                testing_set.append(el)
            elif (self._get_votes_of_user_in_set(training_set, el[0])
                    <self._m):
                training_set.append(el)

        print("Splitted Dataset into {} training and {} testing elements".format(
            len(training_set), len(testing_set)))

        return training_set, testing_set

    def _get_votes_of_user_in_set(self, dataset, user):
        return len([True for el in dataset if el[0] == user])


    def __getattr__(self, name):
        return getattr(self._decoratee, name)
