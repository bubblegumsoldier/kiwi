from asynctest import TestCase, MagicMock, ANY, CoroutineMock
from kiwi.TransferTypes import Vote
from kiwi.database.DataAccessor import DataAccessor
from pandas import DataFrame
from surprise import Dataset
from aiomysql import Connection, Cursor


class DataAccessorTrainsetTest(TestCase):

    def setUp(self):
        connection = MagicMock(spec=Connection)
        cursor = MagicMock(spec=Cursor)
        connection.cursor.return_value = cursor
        cursor.__aenter__ = CoroutineMock(return_value=cursor)

        votes = [
            ('user_a', 'item_a', 0),
            ('user_a', 'item_b', 1),
            ('user_b', 'item_a', 1),
            ('user_b', 'item_b', 1)
        ]
        vote_scale = (0, 1)
        cursor.fetchall = CoroutineMock(return_value=votes)
        cursor.fetchone = CoroutineMock(return_value=vote_scale)
        cursor.execute = CoroutineMock()

        self.accessor = DataAccessor(connection)
        self.connection = connection
        self.cursor = cursor

    async def test_trainset_counts(self):
        trainset = await self.accessor.trainset()

        self.assertEqual(trainset.n_users, 2)
        self.assertEqual(trainset.n_items, 2)
        self.assertEqual(trainset.n_ratings, 4)

    async def test_trainset_items(self):
        trainset = await self.accessor.trainset()

        self.assertCountEqual(
            set(trainset.all_items()),
            list(trainset.all_items())
        )
        outer_item_ids = [
            trainset.to_raw_iid(item)
            for item in trainset.all_items()
        ]
        self.assertSetEqual(
            set(outer_item_ids),
            set(['item_a', 'item_b'])
        )

    async def test_trainset_users(self):
        trainset = await self.accessor.trainset()

        self.assertCountEqual(
            set(trainset.all_users()),
            list(trainset.all_users())
        )
        outer_user_ids = [
            trainset.to_raw_uid(user)
            for user in trainset.all_users()
        ]
        self.assertSetEqual(
            set(outer_user_ids),
            set(['user_a', 'user_b'])
        )


class DataAccessorTest(TestCase):

    def setUp(self):
        connection = MagicMock(spec=Connection)
        cursor = MagicMock(spec=Cursor)
        connection.cursor.return_value = cursor
        cursor.__aenter__ = CoroutineMock(return_value=cursor)
        cursor.execute = CoroutineMock()

        self.accessor = DataAccessor(connection)
        self.connection = connection
        self.cursor = cursor

    async def test_known_user_not_registered_again(self):
        username = 'user_c'
        self.cursor.rowcount = 1  # user is known

        await self.accessor.check_and_register_user(username)

        self.cursor.execute.assert_awaited_once_with(ANY, username)
