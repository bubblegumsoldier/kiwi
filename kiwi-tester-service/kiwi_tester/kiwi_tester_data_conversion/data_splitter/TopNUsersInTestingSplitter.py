import sys
class TopNUsersInTestingSplitter:
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
        top_n_users = self._get_top_n_users(dataset)

        training_set = [vote for vote in dataset if vote[0] not in top_n_users]
        testing_set = [vote for vote in dataset if vote[0] in top_n_users]

        print("Splitted Dataset into {} training and {} testing elements".format(len(training_set), len(testing_set)))

        return training_set, testing_set

    def _get_top_n_users(self, dataset):
        user_vote_table = {}
        for el in dataset:
            if el[0] not in user_vote_table:
                user_vote_table[el[0]] = 1
            else:
                user_vote_table[el[0]] += 1

        import operator
        sorted_user_vote_table = sorted(user_vote_table.items(), key=operator.itemgetter(1))
        best_n_users_with_count = sorted_user_vote_table[-self._n:]
        best_n_users = [x[0] for x in best_n_users_with_count]
        return best_n_users

    def __getattr__(self, name):
        return getattr(self._decoratee, name)