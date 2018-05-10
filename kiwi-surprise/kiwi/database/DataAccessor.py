from aiomysql import IntegrityError
from logging import getLogger
from surprise import Dataset, Reader
import pandas as pd


class DataAccessor:
    def __init__(self, conn=None, rating_scale=(0, 1)):
        self._conn = conn
        self.rating_scale = rating_scale

    async def trainset(self):
        '''
        Currently will return all votes, i.e. will always be the new trainset
        '''
        votes = list(await self._get_votes(self._conn))

        frame = pd.DataFrame.from_records(
            votes, columns=["user", "item", "vote"])

        return Dataset.load_from_df(
            frame,
            Reader(rating_scale=self.rating_scale)
        ).build_full_trainset()

    async def get_unvoted_items(self, uid):
        return await self._get_unvoted(uid, self._conn)

    async def register_user(self, user):
        if not await self._select_user(user, self._conn):
            await self._insert_users([user], self._conn)

    async def batch_register_users(self, users):
        return await self._insert_users(users, self._conn)

    async def insert_votes(self, votes):
        return await self._insert_votes(votes, self._conn)

    async def count_users(self):
        return await self._count_users(self._conn)

    async def count_items(self):
        return await self._count_posts(self._conn)

    async def get_total_votes(self):
        return await self._vote_count(self._conn)

    async def get_voted_and_unvoted_count(self, user):
        voted_count = await self._vote_count_user(user, self._conn)
        post_count = await self._count_posts(self._conn)
        return (voted_count, post_count - voted_count)

    async def store_feedback(self, vote):
        inserted = await self._insert_votes([vote], self._conn)
        return True if inserted == 1 else False

    async def add_content(self, posts):
        return await self._insert_posts(posts, self._conn)

    async def average_rating_count(self):
        return await self._global_rating_count_mean(self._conn)

    async def _insert_votes(self, votes, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(
                'INSERT IGNORE INTO votes (user, product, vote) values(%s, %s, %s)',
                votes)
            return cursor.rowcount

    async def _insert_users(self, users, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(
                'INSERT IGNORE INTO users values(%s)', users)
            return cursor.rowcount

    async def _insert_posts(self, posts, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany('INSERT IGNORE INTO products VALUES(%s)',
                                     posts)
            return cursor.rowcount

    async def _vote_count(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT Count(*) FROM votes v')
            count = await cursor.fetchone()
            return int(count[0])

    async def _vote_count_user(self, username, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT * FROM votes v WHERE v.user = %s',
                                 username)
            return cursor.rowcount

    async def _count_posts(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT COUNT(post_id) FROM products')
            count = await cursor.fetchone()
            return int(count[0])

    async def _count_users(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT COUNT(*) FROM users')
            count = await cursor.fetchone()
            return int(count[0])

    async def _get_unvoted(self, username, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('''
                SELECT DISTINCT p.post_id
                FROM products p
                WHERE p.post_id NOT IN (
                    SELECT votes.product
                    FROM votes
                    WHERE votes.user = %s)''',
                                 username)
            return [row[0] for row in await cursor.fetchall()]

    async def _get_votes(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT user, product, CAST(vote as DECIMAL(3,2)) vote from votes')
            return await cursor.fetchall()

    async def _select_user(self, user, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(
                'SELECT * FROM users WHERE users.uname = %s',
                user)
            return await cursor.fetchone()

    async def _global_rating_count_mean(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT AVG(counts.c) from (SELECT COUNT(*) as                       c from votes v group by v.user) counts')

            avg = await cursor.fetchone()
            return int(avg[0]) if avg[0] else 0
