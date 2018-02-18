from logging import getLogger
from surprise import Dataset, Reader
import pandas as pd


class DataAccessor:
    def __init__(self, trainset=None):
        self.trainset = Dataset.load_builtin('ml-100k').build_full_trainset() \
            if trainset is None \
            else trainset
        self.df = pd.DataFrame.from_records(
            self.trainset.all_ratings(), columns=["user", "item", "vote"])
        self.new_users = set()
        self.new_items = set()  # not used in unvoted_estimation
        self.new_voted = set()

    async def user_in_trainset(self, uid):
        return self.trainset.knows_user(uid)

    async def get_unvoted_items(self, uid):
        unvoted_trained = await self._get_unvoted_from_trainset(uid)
        voted_after_train = {vote.post
                             for vote in self.new_voted
                             if vote.user is uid}
        return list(set(unvoted_trained).difference(voted_after_train))

    async def _get_unvoted_from_trainset(self, uid):
        voted_items = self.df[self.df["user"] == uid]["item"]
        items_series = pd.Series.from_array(self.trainset.all_items())
        return pd.concat([items_series, voted_items]) \
            .drop_duplicates(keep=False) \
            .tolist()

    async def check_and_register_user(self, user):
        if not await self.user_in_trainset(user):
            self.new_users.add(user)

    async def get_unvoted_count(self, user):
        return len(await self.get_unvoted_items(user))

    async def store_feedback(self, vote):
        self.new_voted.add(vote)
        return True

    async def add_content(self, posts):
        self.new_items.update(posts)

    @staticmethod
    def with_updated_trainset(old_set, new_set, scale):
        """
        This prepares an accessor with a new trainset. This will likely need a different signature, once we go to database stored datasets.
        However, the idea of this function should still be the same.

        We combine the old training data (i.e. all ratings that have already been used for training the algorithm) with the new votes we received after the last training step.

        This will add training information about new users and new items, but only if they have rated or have been rated.
        Users and items without interactions will remain unkown.
        Depending on the size of the dataset, it is also likely that there will be no neighbor for a given user. 
        In the movielens-100k set, for example user 40 has no neighbors, because he has no vote overlap to other users (or no correlation).
        """
        new = pd.DataFrame.from_records(
            list(new_set),
            columns=["user", "item", "vote"])

        combined = pd \
            .concat([old_set, new]) \
            .drop_duplicates(keep=False)

        dataset = Dataset.load_from_df(
            combined,
            Reader(rating_scale=scale))

        return DataAccessor(trainset=dataset.build_full_trainset())
