from logging import getLogger
from aiomysql import IntegrityError

RANDOM_SELECT = '''
            SELECT DISTINCT p.post_id
            FROM products p
            WHERE p.post_id NOT IN (
                SELECT votes.product
                FROM votes
                WHERE votes.user = %s)
            ORDER BY upload_time DESC
            '''


class DataAccessor:
    def __init__(self, conn):
        self.conn = conn

    async def check_and_register_user(self, user):
        if not await self._is_user_known(user, self.conn):
            await self._insert_user(user, self.conn)

    async def recommend_for(self, user, count):
        unvoted_posts = await self._get_random_unvoted(
            user, count, self.conn)
        return unvoted_posts

    async def get_unvoted_count(self, user):
        return await self._get_unvoted_count(user, self.conn)

    async def store_feedback(self, vote):
        try:
            await self._insert_vote(vote, self.conn)
            return True
        except IntegrityError as exp:
            getLogger('root').error('Feedback Error: %r', exp)
            return False

    async def add_content(self, posts):
        return await self._insert_posts(posts, self.conn)

    async def _get_random_unvoted(self, username, count, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(RANDOM_SELECT, username)
            products = [row[0] for row in await cursor.fetchmany(count)]
            return {'posts': products,
                    'unvoted': cursor.rowcount,
                    'user': username}

    async def _get_unvoted_count(self, user, conn):
        post_count = await self._count_posts(conn)
        voted = await self._vote_count(user, conn)
        return post_count - voted

    async def _insert_vote(self, vote, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(
                'INSERT INTO votes (user, product, vote) values(%s, %s, %s)',
                vote)

    async def _insert_user(self, username, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('INSERT INTO users values(%s)', username)

    async def _insert_posts(self, posts, conn):
        inserted = 0
        async with conn.cursor() as cursor:
            for post in posts:
                try:
                    await cursor.execute('INSERT INTO products VALUES(%s)',
                                         post)
                    inserted += 1
                except IntegrityError as exp:
                    getLogger('root').error('Content Error:%r', exp)
            return inserted

    async def _is_user_known(self, username, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT * FROM users WHERE users.uname = %s',
                                 username)
            return cursor.rowcount > 0

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
