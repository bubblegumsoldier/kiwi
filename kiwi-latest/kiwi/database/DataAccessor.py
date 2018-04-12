from kiwi.database.AsyncDataAccessor import AsyncDataAccessor

class DataAccessor(AsyncDataAccessor):
    def __init__(self, conn, statements):
        super().__init__(conn, statements)

    async def recommend_for(self, user, count):
        unvoted_posts = await self._get_unvoted_items(
            user, count, self.conn)
        return unvoted_posts

    async def get_ranking(self, item):
        return await self._get_ranking(item, self.conn)

    async def _get_unvoted_items(self, username, count, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(self.stmts['latest_select'], username)
            products = [row[0] for row in await cursor.fetchmany(count)]
            return products

    async def _get_ranking(self, item, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT COUNT(*) FROM products p WHERE p.upload_time < (SELECT upload_time from products where post_id=%s ORDER BY upload_time ASC)', item)
            return (await cursor.fetchone())[0] + 1
