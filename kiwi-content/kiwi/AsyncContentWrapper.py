from kiwi.ContentEngine import ContentEngine
from asyncio import AbstractEventLoop
from pandas import Series

class AsyncContentWrapper:
    def __init__(self, loop: AbstractEventLoop, executor, content_engine: ContentEngine):
        self._loop = loop
        self._content_engine = content_engine
        self._executor = executor

    async def fit(self):
        return await self._loop.run_in_executor(
            self._executor,
            self._content_engine.fit)

    async def build_feature_vectors(self, content=None):
        """
        :content: Pandas dataframe with ItemId Tags (tags as | separated                  substrings). If None, uses the content frame passed to the              engine on creation.
        """
        await self._loop.run_in_executor(
            self._executor,
            self._content_engine.build_feature_vectors,
            content)

    async def build_user_taste_vectors(self, ratings=None):
        """
        User taste vectors for all users in the rating set.

        :ratings:   Dataframe with UserId, ItemId, Like where likes                         values 1 or -1. If None uses rating frame passed
                    in on creation.
        """
        await self._loop.run_in_executor(
            self._executor,
            self._content_engine.build_user_taste_vectors,
            ratings)

    async def build_user_taste_vector(self, user, ratings=None, insert=False):
        return await self._loop.run_in_executor(
            self._executor,
            self._content_engine.build_user_taste_vector,
            user,
            ratings,
            insert)

    async def predict_similarities(self, user, item=None):
        """
        Predicts items that are similar to the users tastes.

        :user: User id of the user in question
        :n: Number of items to suggest. Will be set to 1 if item != None
        :item: Item id of a item that should be estimated.
        :returns: Numpy array of [similarity, itemid]. (shape: n, 2)
        """
        return await self._loop.run_in_executor(
            self._executor, 
            self._content_engine.predict_similarities, 
            user, item)

    async def update_ratings(self, vote):
        self._content_engine.ratings = \
            self._content_engine.ratings.append(Series(vote), ignore_index=True)