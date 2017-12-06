
class Enricher:
    def __init__(self, connection=None):
        self._connection = connection

    async def enrich(self, post_ids):
        return await self._connection.find_many(post_ids)
