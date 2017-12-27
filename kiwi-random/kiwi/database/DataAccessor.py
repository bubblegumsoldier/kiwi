from aiomysql import create_pool
from kiwi.config import read_mysql_config

CONNECTION = read_mysql_config()._asdict()

RANDOM_SELECT = '''
            SELECT DISTINCT p.post_id
            FROM products p
            WHERE p.post_id NOT IN (
                SELECT votes.product
                FROM votes
                WHERE votes.user = %s)
            ORDER BY Rand()
            '''


def wrap_method_into_connection(func):
    async def helper(self, *args, **kwargs):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                result = await func(self, *args, **kwargs, cursor=cur)
                await conn.commit()
                return result
    return helper


class DataAccessor:
    def __init__(self, pool_count=1):
        self.pool_count = pool_count

    async def __aenter__(self):
        self.pool = await create_pool(**CONNECTION, maxsize=self.pool_count)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.pool.close()
        await self.pool.wait_closed()

    @wrap_method_into_connection
    async def get_random_unvoted(self, username, count, cursor=None):
        if cursor:
            await cursor.execute(RANDOM_SELECT, username)
            products = [row[0] for row in await cursor.fetchmany(count)]
            return {'posts': products,
                    'unvoted': cursor.rowcount,
                    'user': username}

    @wrap_method_into_connection
    async def insert_vote(self, vote, cursor=None):
        if cursor:
            await cursor.execute(
                'INSERT INTO votes (user, product, vote) values(%s, %s, %s)',
                vote)

    @wrap_method_into_connection
    async def insert_user(self, username, cursor=None):
        if cursor:
            await cursor.execute('INSERT INTO users values(%s)', username)

    @wrap_method_into_connection
    async def insert_posts(self, posts, cursor=None):
        if cursor:
            await cursor.executemany('INSERT INTO products VALUES(%s)', posts)

    @wrap_method_into_connection
    async def is_user_known(self, username, cursor=None):
        if cursor:
            await cursor.execute('SELECT * FROM users WHERE users.uname = %s',
                                 username)
            return cursor.rowcount > 0

    @wrap_method_into_connection
    async def vote_count(self, username, cursor=None):
        if cursor:
            await cursor.execute('SELECT * FROM votes v WHERE v.user = %s',
                                 username)
            return cursor.rowcount

    @wrap_method_into_connection
    async def count_posts(self, cursor=None):
        if cursor:
            await cursor.execute('SELECT COUNT(post_id) FROM products')
            return (await cursor.fetchone())[0]
