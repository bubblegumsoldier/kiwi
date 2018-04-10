import sys
import random

class RandomPercentageSplitter:
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
            print("RandomPercentageSplitter received dataset looking like: \n")
            import json
            print(json.dumps(dataset, indent=4, sort_keys=True))
        print("Converting with RandomPercentageSplitter")
        return self._split_into_two_sets(dataset)

    def _split_into_two_sets(self, dataset):
        training_set = []
        testing_set = []

        sys.stdout.write('0%')
        for i, l in enumerate(dataset):
            sys.stdout.write('\r')
            sys.stdout.write("{0:.0f}%".format(float(i)/float(len(dataset)) * 100))
            sys.stdout.flush()
            val = random.random()
            if val >= self._training_percentage:
                testing_set.append(l)
            else:
                training_set.append(l)
            
        sys.stdout.write('\r')
        print("Splitted Dataset into {} training and {} testing elements".format(len(training_set), len(testing_set)))

        return training_set, testing_set

    def __getattr__(self, name):
        return getattr(self._decoratee, name)