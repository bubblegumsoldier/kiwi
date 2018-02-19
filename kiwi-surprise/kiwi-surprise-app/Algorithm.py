from itertools import chain
from heapq import nlargest


class Algorithm:
    def __init__(self, loop, executor, algo):
        self.knn = algo
        self._loop = loop
        self._executor = executor

    async def fit(self, trainset):
        """
        Move to other class?
        """
        await self._loop.run_in_executor(None, self.knn.fit, trainset)

    # i believe ids need to be ints, convert this using db?
    async def get_top_n_items(self, uid, iids, n):
        """
        This should use the fitted algorithm to give the closest n items for our user.
        I imagine, that we get all unvoted item ids for the user from the db,
        and use this as the algorithms testset.
        From there we can just pick the top n items.
        We could even store all results until the next training step and just
        use the next highest items from storage (cross-validated with the
        unvoted items). This would reduce the overhead on each request.
        """
        ratings = await self.get_predictions(uid, iids)
        return nlargest(n, ratings, key=lambda r: r[1])

    async def get_predictions(self, uid, iids):
        split_items = [iids[i::4] for i in range(4)]
        return list(chain(*[await self._estimate(uid, items) for items in split_items]))

    async def get_closest_known_user(self, uid, ratings):
        """
        Surprise does not support users that are not known to the trainset at all.
        Therefore we need a method that gives us the closest user in the
        trainset going by the ratings of the current user.
        Then we can impersonate our closest user for the algorithm, while still
        using our new users unvoted items.
        No clue how to do this from the surprise api.
        Would need to modify the similarity calculations of the algorithm to
        only add one row?
        """

    async def _estimate(self, uid, items):
        return await self._loop.run_in_executor(
            self._executor, _inner_estimate, self.knn, uid, items)


def _inner_estimate(knn, uid, items):
    return [(item, *knn.estimate(uid, item)) for item in items]
