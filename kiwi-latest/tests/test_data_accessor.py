# from copy import deepcopy
# from asynctest import TestCase, MagicMock, ANY, CoroutineMock
# from aiomysql import Connection, Cursor, IntegrityError
# from kiwi.database.DataAccessor import DataAccessor
# from kiwi.Types import Vote


# async def mock_dynamic_insertion_execute(query, post):
#     if post['id'] == 'test_post2':
#         raise IntegrityError()


# class DataAccessorTest(TestCase):

#     def setUp(self):
#         connection = MagicMock(spec=Connection)
#         cursor = MagicMock(spec=Cursor)
#         connection.cursor.return_value = cursor
#         cursor.__aenter__ = CoroutineMock(return_value=cursor)
#         cursor.fetchmany = CoroutineMock()

#         self.accessor = DataAccessor(connection)
#         self.connection = connection
#         self.cursor = cursor
#         self.posts = [
#             {'id': 'test_post0'},
#             {'id': 'test_post1'},
#             {'id': 'test_post2'},
#             {'id': 'test_post3'}
#         ]

#     async def test_recommend_for(self):
#         await self.accessor.recommend_for("test_user", 10)
#         self.cursor.__aenter__.assert_called_once()
#         self.cursor.__aexit__.assert_called_once()
#         self.cursor.execute.assert_called_once_with(ANY, "test_user")
#         self.cursor.fetchmany.assert_called_once_with(10)

#     async def test_store_feedback_happy(self):
#         vote = Vote(user='test_user', post='test_post', vote=False)
#         success = await self.accessor.store_feedback(deepcopy(vote))
#         self.cursor.__aenter__.assert_called_once()
#         self.cursor.__aexit__.assert_called_once()
#         self.cursor.execute.assert_called_once_with(ANY, vote)
#         self.assertTrue(success)

#     async def test_store_feedback_except(self):
#         self.cursor.execute = CoroutineMock(side_effect=IntegrityError)
#         vote = Vote(user='test_user', post='test_post', vote=False)
#         success = await self.accessor.store_feedback(deepcopy(vote))
#         self.cursor.__aenter__.assert_called_once()
#         self.cursor.__aexit__.assert_called_once()
#         self.cursor.execute.assert_called_once_with(ANY, vote)
#         self.assertFalse(success)

#     async def test_add_content(self):
#         self.cursor.execute.side_effect = mock_dynamic_insertion_execute
#         inserted = await self.accessor.add_content(self.posts)
#         self.cursor.__aenter__.assert_called_once()
#         self.cursor.__aexit__.assert_called_once()
#         self.assertEqual(self.cursor.execute.call_count, len(self.posts))
#         self.assertEqual(inserted, len(self.posts) - 1)

    
