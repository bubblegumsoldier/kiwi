from aiomysql import IntegrityError
from logging import getLogger
import pandas as pd
import numpy as np


class DataAccessor:
    def __init__(self, conn=None):
        self._conn = conn

    async def get_content_frame(self):
        '''
        Currently will return all votes, i.e. will always be the new trainset
        '''
        data = await self._get_content(self._conn)
        content_frame = pd.DataFrame.from_records(
            data=data, 
            columns=['ItemId', 'Tags'])
        return content_frame

    async def get_unvoted_items(self, uid):
        return await self._get_unvoted(uid, self._conn)

    async def get_vote_frame(self):
        # votes have to be 1, -1 at this point -> adapter somewhere
        return pd.DataFrame(
            await self._get_votes(self._conn), 
            columns=['UserId', 'ItemId', 'Like'])

    async def check_and_register_user(self, user):
        if not await self._is_user_known(user, self._conn):
            await self._insert_user(user, self._conn)

    async def get_voted_and_unvoted_count(self, user):
        voted_count = await self._vote_count(user, self._conn)
        post_count = await self._count_posts(self._conn)
        return (voted_count, post_count - voted_count)

    async def store_feedback(self, vote):
        try:
            await self._insert_vote(vote, self._conn)
            return True
        except IntegrityError as exp:
            getLogger('root').error('Feedback Error: %r', exp)
            return False

    async def add_content(self, posts):
        return await self._insert_posts(posts, self._conn)

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
                    await cursor.execute(
                        'INSERT INTO products (post_id, tags) VALUES(%s, %s)',
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

    async def _get_rating_scale(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT min(vote), max(vote) from votes')
            min_vote, max_vote = await cursor.fetchone()
            getLogger('root').info('%s, %s', min_vote, max_vote)
            return(float(min_vote), float(max_vote))

    async def _get_content(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT post_id, tags from products')
            return list(await cursor.fetchall())


            
