from surprise import Dataset, Reader
from pandas import DataFrame, Series, concat

class BuiltinContext:
    def __init__(self, trainset=None, df=None, users=None, items=None, votes=None):
        self.trainset = Dataset.load_builtin(
            'ml-100k').build_full_trainset() if trainset is None else trainset
        self.df = DataFrame.from_records(
            self.trainset.all_ratings(), columns=["user", "item", "vote"]) if df is None else df
        self.new_users = set() if not users else users
        self.new_items = set() if not items else items
        self.new_voted = set() if not votes else votes

    async def __aenter__(self):
        '''Necessary to use it in the same way as the connection pool'''
        return self

    async def __aexit__(self, exc_t, exc, tb):
        pass

    async def __await__(self):
        return self

    def acquire(self):
        return self

    def close(self):
        pass


class BuiltinDataAccessor:

    def __init__(self, context):
        self._context = context
        self._trainset = context.trainset
        self.df = context.df
        self.new_users = context.new_users
        self.new_items = context.new_items
        self.new_voted = context.new_voted

    async def trainset(self):
        return self._with_updated_trainset()

    async def get_unvoted_items(self, uid):
        unvoted_trained = await self._get_unvoted_from_trainset(uid)
        voted_after_train = {vote.post
                             for vote in self.new_voted
                             if vote.user is uid}
        return list(set(unvoted_trained).difference(voted_after_train))

    async def _get_unvoted_from_trainset(self, uid):
        voted_items = self.df[self.df["user"] == uid]["item"]
        items_series = Series.from_array(self._trainset.all_items())
        return concat([items_series, voted_items]) \
            .drop_duplicates(keep=False) \
            .tolist()

    async def check_and_register_user(self, user):
        if not self._trainset.knows_user(user):
            self.new_users.add(user)

    async def get_voted_and_unvoted_count(self, user):
        unvoted = len(await self.get_unvoted_items(user))
        voted = len(self.df[self.df["user"] == user]["item"])
        return (unvoted, voted)

    async def store_feedback(self, vote):
        self.new_voted.add(vote)
        return True

    async def add_content(self, posts):
        self.new_items.update(posts)

    def _with_updated_trainset(self):
        """
        This prepares an accessor with a new trainset. This will likely need a different signature, once we go to database stored datasets.
        However, the idea of this function should still be the same.

        We combine the old training data (i.e. all ratings that have already been used for training the algorithm) with the new votes we received after the last training step.

        This will add training information about new users and new items, but only if they have rated or have been rated.
        Users and items without interactions will remain unkown.
        Depending on the size of the dataset, it is also likely that there will be no neighbor for a given user.
        In the movielens-100k set, for example user 40 has no neighbors, because he has no vote overlap to other users (or no correlation).
        """
        new = DataFrame.from_records(
            list(self.new_voted),
            columns=["user", "item", "vote", "timestamp"])

        combined = concat([self.df, new])

        dataset = Dataset.load_from_df(
            combined,
            Reader(rating_scale=self._trainset.rating_scale))

        return dataset.build_full_trainset()