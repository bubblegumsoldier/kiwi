from copy import deepcopy


class CollectionManipulator:
    def __init__(self, mongo_collection):
        self.collection = mongo_collection

    async def insert_posts(self, posts):
        await self.collection.insert_many(deepcopy(posts))
        return posts

    async def post_exists(self, post_id):
        return (await self.collection.find_one({'id': post_id})) is not None
