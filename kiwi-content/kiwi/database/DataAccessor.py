from aiomysql import IntegrityError
from logging import getLogger
import pandas as pd
import numpy as np


class DataAccessor:
    def __init__(self, conn=None):
        self._conn = conn

    async def get_content_frame(self):
        data = await self._get_content(self._conn)
        content_frame = pd.DataFrame.from_records(
            data=data,
            columns=['ItemId', 'Tags'])
        return content_frame

    async def insert_votes(self, votes):
        return await self._insert_votes(votes, self._conn)

    async def get_unvoted_items(self, uid):
        return await self._get_unvoted(uid, self._conn)

    async def get_vote_frame(self):
        # votes have to be 1, -1 at this point -> adapter somewhere
        return pd.DataFrame(
            await self._get_votes(self._conn),
            columns=['UserId', 'ItemId', 'Like'])

    async def register_user(self, user):
        await self._insert_users([user], self._conn)

    async def batch_register_users(self, users):
        return await self._insert_users(users, self._conn)

    async def get_voted_and_unvoted_count(self, user):
        voted_count = await self._vote_count(user, self._conn)
        post_count = await self._count_posts(self._conn)
        return (voted_count, post_count - voted_count)

    async def store_feedback(self, vote):
        inserted = await self._insert_votes([vote], self._conn)
        return True if inserted == 1 else False

    async def add_content(self, posts):
        return await self._insert_posts(posts, self._conn)

    async def _insert_votes(self, vote, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(
                'INSERT IGNORE INTO votes (user, product, vote) values(%s, %s, %s)',
                vote)
            return cursor.rowcount

    async def _insert_users(self, users, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany('INSERT IGNORE INTO users values(%s)', users)
            return cursor.rowcount

    async def _insert_posts(self, posts, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(
                'INSERT IGNORE INTO products (post_id, tags) VALUES(%s, %s)', posts)
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
            return np.array([r[0] for r in await cursor.fetchall()])

    async def _get_votes(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT user, product, vote from votes')
            return list(await cursor.fetchall())

    async def _get_content(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT post_id, tags from products')
            return list(await cursor.fetchall())
