from asynctest import TestCase, MagicMock

from app.DatabaseConnection import CollectionManipulator
from motor.motor_asyncio import AsyncIOMotorCollection


stored_posts = [
    {'id': 1},
    {'id': 2},
    {'id': 3}
]


async def mocked_find_one(post):
    if post in stored_posts:
        return post
    return None

# Mongo adds _id to each post. We don't want that in our original posts.


async def mocked_insert_many(posts):
    for index, post in enumerate(posts):
        post['_id'] = post['id'] + index


class TestCollection(TestCase):
    def setUp(self):
        collection = MagicMock(AsyncIOMotorCollection)
        collection.find_one.side_effect = mocked_find_one
        collection.insert_many.side_effect = mocked_insert_many
        self.collection = collection
        self.manipulator = CollectionManipulator(collection)

    async def test_post_exists(self):
        exists = await self.manipulator.post_exists(1)
        self.collection.find_one.assert_called_once_with({'id': 1})
        self.assertEqual(exists, True)

    async def test_post_exists_not(self):
        post = {'id': 4}
        exists = await self.manipulator.post_exists(4)
        self.collection.find_one.assert_called_once_with(post)
        self.assertEqual(exists, False)

    async def test_insert_does_not_change_input(self):
        posts = [{'id': 1},
                 {'id': 2},
                 {'id': 3}]
        await self.manipulator.insert_posts(posts)
        self.assertEqual(posts, stored_posts)
        self.collection.insert_many.assert_called_once()
