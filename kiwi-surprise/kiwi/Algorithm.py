from itertools import chain
from heapq import nlargest


class AlgorithmWrapper:
    def __init__(self, loop, executor, algo):
        self.knn = algo
        self._loop = loop
        self._executor = executor
        self._trainset = None

    async def fit(self, trainset):
        """
        Move to other class?
        """
        self._trainset = trainset
        await self._loop.run_in_executor(None, self.knn.fit, trainset)

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

    async def predict(self, uid, iid):
        return self.knn.predict(uid, iid, clip=True)

    async def get_rating_density(self):
        n_users = self._trainset.n_users
        n_items = self._trainset.n_items
        n_ratings = self._trainset.n_ratings
        try:
            return n_ratings / (n_items * n_users)
        except ZeroDivisionError:
            return 0

    async def get_rating_count(self):
        return self._trainset.n_ratings

    async def _estimate(self, uid, items):
        return await self._loop.run_in_executor(
            self._executor, _inner_estimate, self.knn, uid, items)


def _inner_estimate(knn, uid, items):
    return [(item, *knn.predict(uid, item, clip=False)) for item in items]
