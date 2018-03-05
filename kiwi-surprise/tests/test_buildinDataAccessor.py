from asynctest import TestCase, MagicMock, ANY, CoroutineMock
from kiwi.TransferTypes import Vote
from kiwi.database.BuiltinDataAccessor import (BuiltinDataAccessor, BuiltinContext)
from pandas import DataFrame
from surprise import Dataset


class DataAccessorTest(TestCase):

    def setUp(self):
        self.context = BuiltinContext()  # use ml-100k
        self.accessor = BuiltinDataAccessor(context=self.context)
        self.base_trainset = Dataset.load_builtin(
            'ml-100k').build_full_trainset()
        self.uid = 0
        self.test_vote = Vote(user=self.uid, post=1, vote=3)

    async def test_return_unvoted_items_without_votes(self):
        unvoted_items = await self.accessor.get_unvoted_items(self.uid)
        voted_items = [rating[0] for rating in self.base_trainset.ur[self.uid]]
        self.assertEqual(
            len(unvoted_items),
            self.base_trainset.n_items - len(voted_items))
        intersect = set(unvoted_items).intersection(voted_items)
        self.assertSetEqual(intersect, set())

    async def test_return_unvoted_items_with_vote(self):
        # Post 1 is not voted by user 0 in ml-100k dataset
        await self.accessor.store_feedback(self.test_vote)
        unvoted_items = await self.accessor.get_unvoted_items(self.uid)
        self.assertNotIn(1, unvoted_items)

    async def test_updated_trainset_contains_new_voted(self):
        await self.accessor.store_feedback(self.test_vote)
        updated_trainset = await self.accessor.trainset()
        self.assertEqual(updated_trainset.n_ratings, 100001)
        user_inner_id = updated_trainset.to_inner_uid(self.uid)
        item_inner_id = updated_trainset.to_inner_iid(self.test_vote.post)
        self.assertIn(
            (item_inner_id, self.test_vote.vote),
            updated_trainset.ur[user_inner_id])

    
       
