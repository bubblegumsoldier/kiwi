from os import environ
from itertools import chain
from collections import namedtuple
from aiomysql import connect


CONNECTION = {
    "host": 'localhost',
    "port": 3306,
    "user": environ['MSQL_USER'],
    "password": environ['MSQL_PWD'],
    "db": "random_recommender"
}

RANDOM_SELECT = """
            SELECT p.post_id
            FROM products p
            WHERE p.post_id NOT IN (
                SELECT votes.product
                FROM votes
                WHERE votes.user = %s)
            ORDER BY Rand()
            """


def wrap_into_connection(func):
    async def helper(*args, **kwargs):
        async with connect(**CONNECTION) as conn:
            async with conn.cursor() as cur:
                return await func(*args, **kwargs, conn=conn, cur=cur)

    return helper


@wrap_into_connection
async def get_random_unvoted(user, conn=None, cur=None):
    if cur:
        await cur.execute(RANDOM_SELECT, [user.name])
        products = [row[0] for row in await cur.fetchmany(2)]
        unseen = cur.rowcount - 2
        return {"posts": products, "unseen":unseen}


@wrap_into_connection
async def insert_vote(vote, conn=None, cur=None):
    if conn and cur:
        await cur.execute("INSERT INTO votes values(%s, %s, %s)", vote)
        await conn.commit()


@wrap_into_connection
async def insert_user(user, conn=None, cur=None):
    if conn and cur:
        await cur.execute("INSERT INTO users values(%s)", [*user])
        await conn.commit()


@wrap_into_connection
async def insert_posts(posts, conn=None, cur=None):
    if conn and cur:
        await cur.executemany("INSERT INTO products VALUES(%s)", posts)
        await conn.commit()


@wrap_into_connection
async def is_user_known(user, conn=None, cur=None):
    if cur:
        await cur.execute("SELECT * FROM users WHERE users.uname = %s", [user.name])
        return cur.rowcount > 0
