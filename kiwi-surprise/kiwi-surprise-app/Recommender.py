import algorithm_persistence_tools
import os
from surprise import BaselineOnly
from surprise import Dataset
from surprise import Reader
import csv_reader

class Recommender:
    def __init__(self, data_accessor):
        self.accessor = data_accessor

    async def recommend_for(self, user, count=10):
        algorithm = algorithm_persistence_tools.load_algorithm()
        data = await self.get_data()
        trainset = data.build_full_trainset()
        algorithm.predict()
        return await self.accessor.recommend_for(user, count)

    async def get_data(self):
        # path to dataset file
        file_path = csv_reader.get_data_path()

        # As we're loading a custom dataset, we need to define a reader. In the
        # movielens-100k dataset, each line has the following format:
        # 'user item rating timestamp', separated by '\t' characters.
        reader = Reader(line_format='user item rating timestamp', sep='\t')
        data = Dataset.load_from_file(file_path, reader=reader)
        return data

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        success = await self.accessor.store_feedback(vote)
        unvoted = await self.accessor.get_unvoted_count(vote.user)
        if success:
            return {'user': vote.user, 'post': vote.post, 'unvoted': unvoted}
        return {}

    async def add_content(self, posts):
        filtered_posts = [post['id'] for post in posts]
        inserted = await self.accessor.add_content(filtered_posts)
        return {'inserted_count': inserted}

    async def _register_user(self, user):
        await self.accessor.check_and_register_user(user)
