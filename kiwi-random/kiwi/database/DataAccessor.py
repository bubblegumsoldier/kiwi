from logging import getLogger
from aiomysql import IntegrityError

RANDOM_SELECT = '''
            SELECT DISTINCT p.post_id
            FROM products p
            WHERE p.post_id NOT IN (
                SELECT votes.product
                FROM votes
                WHERE votes.user = %s)
            ORDER BY Rand()
            '''


class DataAccessor:
    def __init__(self, conn):
        self.conn = conn

    async def register_user(self, user):
        if not self._select_user(user, self.conn):
            await self._insert_users([user], self.conn)

    async def batch_register_users(self, users):
        return await self._insert_users(users, self.conn)

    async def recommend_for(self, user, count):
        unvoted_posts = await self._get_random_unvoted(
            user, count, self.conn)
        return unvoted_posts

    async def get_voted_and_unvoted_count(self, user):
        return await self._get_voted_and_unvoted_count(user, self.conn)

    async def insert_votes(self, votes):
        return await self._insert_votes(votes, self.conn)

    async def store_feedback(self, vote):
        inserted = await self._insert_votes([vote], self.conn)
        return True if inserted == 1 else False

    async def add_content(self, posts):
        return await self._insert_posts(posts, self.conn)

    async def get_post_count(self):
        return await self._count_posts(self.conn)

    async def get_mean_and_std(self):
        return await self._get_mean_and_std(self.conn)

    async def _get_random_unvoted(self, username, count, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(RANDOM_SELECT, username)
            products = [row[0] for row in await cursor.fetchmany(count)]
            return products

    async def _get_voted_and_unvoted_count(self, user, conn):
        post_count = await self._count_posts(conn)
        voted = await self._vote_count(user, conn)
        return (voted, post_count - voted)

    async def _insert_votes(self, votes, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(
                'INSERT IGNORE INTO votes (user, product, vote) values(%s, %s, %s)',
                votes)
            return cursor.rowcount

    async def _insert_users(self, users, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany('INSERT IGNORE INTO users values(%s)', users)
            return cursor.rowcount

    async def _insert_posts(self, posts, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(
                'INSERT IGNORE INTO products VALUES(%s)', posts)
            return cursor.rowcount

    async def _vote_count(self, username, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT * FROM votes v WHERE v.user = %s',
                                 username)
            return cursor.rowcount

    async def _count_posts(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT COUNT(post_id) FROM products')
            count = await cursor.fetchone()
            return int(count[0])

    async def _get_mean_and_std(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT AVG(vote), STD(vote) FROM votes')
            dist = await cursor.fetchone()
            return (float(dist[0]) if dist else 0,
                    float(dist[1]) if dist else 0)

    async def _select_user(self, user, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(
                'SELECT * FROM users WHERE users.uname = %s',
                user)
            return await cursor.fetchone()
