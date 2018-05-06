from kiwi.ContentEngine import ContentEngine
from asyncio import AbstractEventLoop
from logging import getLogger


class AsyncContentWrapper:
    def __init__(self, loop: AbstractEventLoop, executor, content_engine: ContentEngine):
        self._loop = loop
        self._content_engine = content_engine
        self._executor = executor

    async def fit(self):
        try:
            return await self._loop.run_in_executor(
                self._executor,
                self._content_engine.fit)
        except ValueError as e:
            getLogger('error').info(
                "Fitting unsuccessful, likely because no items are present")
            getLogger('error').warn(e)

    async def build_feature_vectors(self):
        """
        :content: Pandas dataframe with ItemId Tags (tags as | separated                  substrings). If None, uses the content frame passed to the              engine on creation.
        """
        await self._loop.run_in_executor(
            self._executor,
            self._content_engine.build_feature_vectors)

    async def build_user_taste_vectors(self):
        """
        User taste vectors for all users in the rating set.

        :ratings:   Dataframe with UserId, ItemId, Like where likes                         values 1 or -1. If None uses rating frame passed
                    in on creation.
        """
        await self._loop.run_in_executor(
            self._executor,
            self._content_engine.build_user_taste_vectors)

    async def build_user_taste_vector(self, user, insert=False):
        try:
            return await self._loop.run_in_executor(
                self._executor,
                self._content_engine.build_user_taste_vector,
                user,
                insert)
        except ValueError:
            getLogger('error').warn(
                'Error during user taste vector building, likely no known content present')
            raise Exception(
                'Cannot build user taste vector. Feedback not stored.')

    async def predict_similarities(self, user, item=None):
        """
        Predicts items that are similar to the users tastes.

        :user: User id of the user in question
        :n: Number of items to suggest. Will be set to 1 if item != None
        :item: Item id of a item that should be estimated.
        :returns: Numpy array of [similarity, itemid]. (shape: n, 2)
        """
        try:
            return await self._loop.run_in_executor(
                self._executor,
                self._content_engine.predict_similarities,
                user, item)
        except ValueError:
            raise Exception('Cannot calculate recommendations, algorithm has not been initialized correctly. Maybe add content?')


    async def update_ratings(self, vote):
        self._content_engine.update_ratings(vote)

    async def get_user_taste_vector(self, uid):
        try:
            return self._content_engine.user_vectors.loc[uid]
        except KeyError:
            raise KeyError('User does not exist')
