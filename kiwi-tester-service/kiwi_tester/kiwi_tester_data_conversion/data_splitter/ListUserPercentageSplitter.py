import sys
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
        two_sets = self._split_into_two_sets(dataset)
        users_of_0 = [el[0] for el in two_sets[0]]
        users_of_1 = [el[0] for el in two_sets[1]]
        for el in users_of_0:
            if not el in users_of_0:
                print(el)
        
        return two_sets

    def _split_into_two_sets(self, dataset):
        training_set = []
        testing_set = []

        sys.stdout.write('0%')
        for i, l in enumerate(dataset):
            sys.stdout.write('\r')
            sys.stdout.write("{0:.0f}%".format(float(i)/float(len(dataset)) * 100))
            sys.stdout.flush()

            username = l[0]
            next_reached_training_ratio = float(self._get_number_of_votes_for_user_in_dataset(username, training_set)) / float(self._get_number_of_votes_for_user_in_dataset(username, dataset))
            if next_reached_training_ratio > self._training_percentage:
                testing_set.append(l)
            else:
                training_set.append(l)
        sys.stdout.write('\r')
        print("Splitted Dataset into {} training and {} testing elements".format(len(training_set), len(testing_set)))

        return training_set, testing_set

    def _get_number_of_votes_for_user_in_dataset(self, user, dataset):
        votes_of_user = [True for u in dataset if u[0] == user]
        return len(votes_of_user)

    def __getattr__(self, name):
        return getattr(self._decoratee, name)