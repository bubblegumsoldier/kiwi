from motor.motor_asyncio import AsyncIOMotorClient
from os import environ

def get_connection():
    connection_string = 'mongodb://{user}:{pwd}@{host}:{port}'.format(
        user=environ['MONGO_USER'],
        pwd=environ['MONGO_PWD'],
        host=environ['MONGO_HOST'],
        port=environ['MONGO_PORT'])
    client = AsyncIOMotorClient(connection_string)
    db = client[environ['MONGO_DB']]
    return MongoConnection(db, environ['MONGO_COLLECTION'])


class MongoConnection:
    def __init__(self, db, collection):
        self._db = db
        self._collection = db[collection]

    async def find_document(self, doc_id):
        enriched = await self._collection.find_one(
            {'id': doc_id},
            projection={'_id': False, 'title': True, 'link': True, 'id': True, 'type': True, 'mp4': True})
        if enriched:
            if enriched['type'] == "image/gif" and 'mp4' in enriched and enriched.get('mp4'):
                enriched['src'] = enriched.pop('mp4')
            else:
                enriched['src'] = enriched.pop('link')
        return enriched

    async def find_many(self, doc_ids):
        posts = [await self.find_document(doc_id) for doc_id in doc_ids]
        return [post for post in posts if post]

    def close(self):
        self._db.client.close()
