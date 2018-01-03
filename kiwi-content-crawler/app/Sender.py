
class Sender:
    def __init__(self, session, url, collection):
        self._session = session
        self._url = url
        self._collection = collection

    async def store_posts_and_send(self, posts):
        await self._collection.insert_posts(posts)
        async with self._session.post(self._url, json={'posts': posts}):
            return
