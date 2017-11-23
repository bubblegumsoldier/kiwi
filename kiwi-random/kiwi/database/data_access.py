from os import environ
from aiomysql import connect
from kiwi.Logging import log_exception
from pymysql.err import OperationalError, IntegrityError

CONNECTION = {
    "host": environ['MSQL_HOST'],
    "port": int(environ['MSQL_PORT']),
    "user": environ['MSQL_USER'],
    "password": environ['MSQL_PWD'],
    "db": environ['MSQL_DATABASE']
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
    @log_exception(exceptions=(OperationalError))
    async def helper(*args, **kwargs):
        async with connect(**CONNECTION) as conn:
            async with conn.cursor() as cur:
                return await func(*args, **kwargs, conn=conn, cur=cur)
    return helper


@wrap_into_connection
@log_exception(exceptions=(IntegrityError))
async def get_random_unvoted(username, count, conn=None, cur=None):
    if cur:
        await cur.execute(RANDOM_SELECT, username)
        products = [row[0] for row in await cur.fetchmany(count)]

        return {"posts": products,
                "unvoted": cur.rowcount,
                "user": username}


@wrap_into_connection
@log_exception(exceptions=(IntegrityError))
async def insert_vote(vote, conn=None, cur=None):
    if conn and cur:
        await cur.execute(
            "INSERT INTO votes (user, product, vote) values(%s, %s, %s)", vote)
        await conn.commit()


@wrap_into_connection
@log_exception(exceptions=(IntegrityError))
async def insert_user(username, conn=None, cur=None):
    if conn and cur:
        await cur.execute("INSERT INTO users values(%s)", username)
        await conn.commit()


@wrap_into_connection
@log_exception(exceptions=(IntegrityError))
async def insert_posts(posts, conn=None, cur=None):
    if conn and cur:
        await cur.executemany("INSERT INTO products VALUES(%s)", posts)
        await conn.commit()


@wrap_into_connection
@log_exception(exceptions=(IntegrityError))
async def is_user_known(username, conn=None, cur=None):
    if cur:
        await cur.execute("SELECT * FROM users WHERE users.uname = %s",
                          username)
        return cur.rowcount > 0


@wrap_into_connection
@log_exception(exceptions=(IntegrityError))
async def vote_count(username, conn=None, cur=None):
    if cur:
        await cur.execute("SELECT * FROM votes v WHERE v.user = %s", username)
        return cur.rowcount
