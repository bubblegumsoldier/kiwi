import asyncio
from os import environ
from itertools import chain
from collections import namedtuple
from aiomysql import connect, Connection, Cursor


ConnectValues = namedtuple('ConnectValues', 'host user password db port')

# config
connectionStr = ConnectValues(
    host='localhost',
    port=3306,
    user=environ['MSQL_USER'],
    password=environ['MSQL_PWD'],
    db="random_recommender"
)

select = """SELECT p.post_id 
            FROM products p 
            WHERE p.post_id NOT IN (
                SELECT votes.product 
                FROM votes 
                WHERE votes.user = %s) 
            ORDER BY Rand() 
            LIMIT %s"""


async def get_random_unvoted(user):
    async with connect(*connectionStr,
                       loop=asyncio.get_event_loop()) as conn:  # type: Connection
        async with conn.cursor() as cur:  # type: Cursor

            await cur.execute(select, [user.name, 2])
            product = list(chain(await cur.fetchall()))
            return product


async def insert_vote(vote):
    async with connect(*connectionStr,
                       loop=asyncio.get_event_loop()) as conn:  # type: Connection
        async with conn.cursor() as cur:  # type: Cursor
            await cur.execute("INSERT INTO votes values(%s, %s, %s)", vote)
            await conn.commit()
