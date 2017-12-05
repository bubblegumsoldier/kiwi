

class Enricher:
    def __init__(self, connection=None):
        self._connection = connection

    async def enrich(self, post_ids):
        return [{'title': 'lorem', 'description': 'ipsum', 'id': post_id}
                for post_id
                in post_ids]
