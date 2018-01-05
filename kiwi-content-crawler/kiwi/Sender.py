from logging import getLogger

class Sender:
    def __init__(self, session, url, collection):
        self._session = session
        self._url = url
        self._collection = collection

    async def store_posts_and_send(self, posts):
        getLogger("root").info("Sending...")
        async with self._session.post(self._url, json={'posts': posts}) as resp:
            await self._collection.insert_posts(posts)
