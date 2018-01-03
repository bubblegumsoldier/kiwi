from copy import deepcopy


class CollectionManipulator:
    def __init__(self, mongo_collection):
        self.collection = mongo_collection

    async def insert_posts(self, posts):
        await self.collection.insert_many(deepcopy(posts))
        return posts

    async def get_post(self, post_id):
        document = await self.collection.find_one({'_id': post_id})
        return document  # potentially none

    async def get_many(self, post_ids):
        docs = [await self.get_post(post_id) for post_id in post_ids]
        return filter(lambda x: x is not None, docs)

    async def post_exists(self, post_id):
        return (await self.collection.find_one({'id': post_id})) is not None
