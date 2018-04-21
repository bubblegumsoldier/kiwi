from logging import getLogger
from aiomysql import IntegrityError


class AsyncDataAccessor:
    def __init__(self, conn, statements):
        """
        Conn is a connection object from aiomysql.
        Statements is a dict, which contains sql templates.
        """
        self.conn = conn
        self.stmts = statements

    async def register_user(self, user):
        if not await self._select_user(user, self.conn):
            return await self._insert_users([user], self.conn)

    async def batch_register_users(self, users):
        return await self._insert_users(users, self.conn)

    async def store_feedback(self, vote):
        inserted = await self._insert_vote(vote, self.conn)
        return True if inserted == 1 else False

    async def add_content(self, posts):
        return await self._insert_posts(posts, self.conn)

    async def insert_votes(self, votes):
        return await self._insert_votes(votes, self.conn)

    async def get_voted_and_total_count(self, user):
        total = await self._count_posts(self.conn)
        voted = await self._count_votes(user, self.conn)
        return (voted, total)

    async def get_voted_and_unvoted_count(self, user):
        total, voted = await self.get_voted_and_total_count(user)
        return (voted, (total-voted))

    async def _select_user(self, user, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(self.stmts['select_user'], user)
            return await cursor.fetchone()

    async def _count_posts(self, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(self.stmts['count_posts'])
            count = await cursor.fetchone()
            return int(count[0])

    async def _count_votes(self, user, conn):
        async with conn.cursor() as cursor:
            await cursor.execute(self.stmts['count_votes'],
                                 user)
            count = await cursor.fetchone()
            return int(count[0])

    async def _insert_users(self, users, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(self.stmts['insert_user'], users)
            return cursor.rowcount

    async def _insert_vote(self, vote, conn):
        return await self._insert_votes([vote], conn)

    async def _insert_votes(self, votes, conn):
        async with conn.cursor() as cursor:
            print(votes)
            await cursor.executemany(self.stmts['insert_vote'], votes)
            return cursor.rowcount

    async def _insert_posts(self, posts, conn):
        async with conn.cursor() as cursor:
            await cursor.executemany(self.stmts['insert_item'], posts)
            return cursor.rowcount
