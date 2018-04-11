from numpy.random import normal


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
            'recommendations': recs,
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
        mean, std = await self.accessor.get_mean_and_std()
        voted, unvoted = await self.accessor.get_voted_and_unvoted_count(user)
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
        await self.accessor.check_and_register_user(user)
