from aiomysql import IntegrityError
from logging import getLogger
from surprise import Dataset, Reader
import pandas as pd


class BuiltinContext:
    def __init__(self, trainset=None, df=None, users=None, items=None, votes=None):
        self.trainset = Dataset.load_builtin(
            'ml-100k').build_full_trainset() if trainset is None else trainset
        self.df = pd.DataFrame.from_records(
            self.trainset.all_ratings(), columns=["user", "item", "vote"]) if df is None else df
        self.new_users = set() if not users else users
        self.new_items = set() if not items else items
        self.new_voted = set() if not votes else votes

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_t, exc, tb):
        pass

    async def __await__(self):
        return self

    def acquire(self):
        return BuiltinContext(
            trainset=self.trainset,
            df=self.df,
            users=self.new_users,
            items=self.new_items,
            votes=self.new_voted)

    def close(self):
        pass


class BuiltinDataAccessor:

    def __init__(self, context):
        self._trainset = context.trainset
        self.df = context.df
        self.new_users = context.new_users
        self.new_items = context.new_items
        self.new_voted = context.new_voted

    async def trainset(self):
        return self._with_updated_trainset()

    async def get_unvoted_items(self, uid):
        unvoted_trained = await self._get_unvoted_from_trainset(uid)
        voted_after_train = {vote.post
                             for vote in self.new_voted
                             if vote.user is uid}
        return list(set(unvoted_trained).difference(voted_after_train))

    async def _get_unvoted_from_trainset(self, uid):
        voted_items = self.df[self.df["user"] == uid]["item"]
        items_series = pd.Series.from_array(self._trainset.all_items())
        return pd.concat([items_series, voted_items]) \
            .drop_duplicates(keep=False) \
            .tolist()

    async def check_and_register_user(self, user):
        if not self._trainset.knows_user(user):
            self.new_users.add(user)

    async def get_unvoted_count(self, user):
        return len(await self.get_unvoted_items(user))

    async def store_feedback(self, vote):
        self.new_voted.add(vote)
        return True

    async def add_content(self, posts):
        self.new_items.update(posts)

    def _with_updated_trainset(self):
        """
        This prepares an accessor with a new trainset. This will likely need a different signature, once we go to database stored datasets.
        However, the idea of this function should still be the same.

        We combine the old training data (i.e. all ratings that have already been used for training the algorithm) with the new votes we received after the last training step.

        This will add training information about new users and new items, but only if they have rated or have been rated.
        Users and items without interactions will remain unkown.
        Depending on the size of the dataset, it is also likely that there will be no neighbor for a given user.
        In the movielens-100k set, for example user 40 has no neighbors, because he has no vote overlap to other users (or no correlation).
        """
        new = pd.DataFrame.from_records(
            list(self.new_voted),
            columns=["user", "item", "vote"])

        combined = pd \
            .concat([self.df, new]) \
            .drop_duplicates(keep=False)

        dataset = Dataset.load_from_df(
            combined,
            Reader(rating_scale=self._trainset.rating_scale))

        return dataset.build_full_trainset()


class DataAccessor:
    def __init__(self, conn=None):
        self._conn = conn

    async def trainset(self):
        '''
        Currently will return all votes, i.e. will always be the new trainset
        '''
        return await self._get_votes(self._conn)

    async def user_in_trainset(self, user):
        pass

    async def get_unvoted_items(self, uid):
        return await self._get_unvoted(uid, self._conn)

    async def check_and_register_user(self, user):
        if not self._is_user_known(user, self._conn):
            self._insert_user(user, self._conn)

    async def get_unvoted_count(self, user):
        voted_count = await self._vote_count(user, self._conn)
        post_count = await self._count_posts(self._conn)
        return post_count - voted_count

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
            await cursor.execute('SELECT * from votes')
            return await cursor.fetchall()
