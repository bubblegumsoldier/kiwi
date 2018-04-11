from asynctest import TestCase, MagicMock, CoroutineMock
from kiwi.recommender.Recommender import Recommender
from kiwi.database.DataAccessor import DataAccessor


class TestRecommender(TestCase):

    def setUp(self):
        self.accessor = MagicMock(spec=DataAccessor)
        self.accessor.get_post_count = CoroutineMock(return_value=5)
        self.accessor.get_unvoted_count = CoroutineMock(return_value=3)

    async def test_predict_for_ranking(self):
        self.accessor.get_ranking = CoroutineMock(return_value=2)
        recommender = Recommender(self.accessor, min_rating=1, max_rating=5)

        val = await recommender.predict_for('u1', 'i1')
        self.assertEqual(val['prediction'], 3.0)
        self.accessor.get_ranking.assert_called_once_with('i1')

    async def test_predict_min_rating(self):
        self.accessor.get_ranking = CoroutineMock(return_value=5)
        recommender = Recommender(self.accessor, min_rating=1, max_rating=5)

        val = await recommender.predict_for('u1', 'i1')
        self.assertEqual(val['prediction'], 1.0)
        self.accessor.get_ranking.assert_called_once_with('i1')
