from numpy.random import normal
from statistics import mean, stdev

class Recommender:
    def __init__(self, data_accessor, min_rating=0, max_rating=1):
        self.accessor = data_accessor
        self.min_rating = min_rating
        self.max_rating = max_rating

    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        recs = await self.accessor.recommend_for(user, count)
        voted, unvoted = await self.accessor.get_voted_and_unvoted_count(user)
        return {
            'posts': recs,
            'user': user,
            'voted': voted,
            'unvoted': unvoted
        }

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        success = await self.accessor.store_feedback(vote)
        voted, unvoted = \
            await self.accessor.get_voted_and_unvoted_count(vote.user)
        if success:
            return {
                'user': vote.user,
                'post': vote.post,
                'unvoted': unvoted,
                'voted': voted}
        return {}

    async def add_content(self, posts):
        filtered_posts = [post['id'] for post in posts]
        inserted = await self.accessor.add_content(filtered_posts)
        return {'inserted_count': inserted}

    async def predict_for(self, user, item):
        voted, unvoted = await self.accessor.get_voted_and_unvoted_count(user)
        mean, std = await self._get_current_rating_spread()
        prediction = min([
            max([normal(mean, std), self.min_rating]),
            self.max_rating])
        return {
            'prediction': prediction,
            'user': user,
            'post': item,
            'unvoted': unvoted,
            'voted': voted
        }

    async def _register_user(self, user):
        await self.accessor.register_user(user)


    async def _get_current_rating_spread(self):
        avg, std = await self.accessor.get_mean_and_std()
        if avg == 0 and std == 0:
            avg = mean([self.min_rating, self.max_rating])
            std = stdev([self.min_rating, self.max_rating])
        return avg, std/2
        