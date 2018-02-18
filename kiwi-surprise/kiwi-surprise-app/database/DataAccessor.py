from logging import getLogger
from surprise import Dataset
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

    async def with_updated_trainset(self):
        new = pd.DataFrame.from_records(self.new_voted)
        combined = self.df.concat(new).drop_duplicates(keep=False).tolist()
        return DataAccessor(trainset=combined)
