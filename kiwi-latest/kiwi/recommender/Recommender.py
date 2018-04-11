
class Recommender:
    def __init__(self, data_accessor, min_rating=0, max_rating=1):
        self.accessor = data_accessor
        self.min = min_rating
        self.max = max_rating


    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        recommendations = await self.accessor.recommend_for(user, count)
        total_count, unvoted_count = await self._get_total_and_unvoted(user)
        return {
            'user': user,
            'recommendations': recommendations,
            'unvoted': unvoted_count,
            'voted': total_count - unvoted_count
        }

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        success = await self.accessor.store_feedback(vote)
        total_count, unvoted_count = \
            await self._get_total_and_unvoted(vote.user)
        if success:
            return {
                'user': vote.user,
                'post': vote.post,
                'unvoted': unvoted_count,
                'voted': total_count - unvoted_count}
        return {}

    async def add_content(self, posts):
        filtered_posts = [post['id'] for post in posts]
        inserted = await self.accessor.add_content(filtered_posts)
        return {'inserted_count': inserted}

    async def predict_for(self, user, item):
        total_count, unvoted_count = await self._get_total_and_unvoted(user)
        ranking = await self.accessor.get_ranking(item)

        prediction = max(
            [self.max * (1 - ranking / total_count), self.min])
        return {
            'prediction': prediction,
            'user': user,
            'post': item,
            'voted': total_count - unvoted_count,
            'unvoted': unvoted_count
        }

    async def _register_user(self, user):
        await self.accessor.check_and_register_user(user)

    async def _get_total_and_unvoted(self, user):
        total_count = await self.accessor.get_post_count()
        unvoted_count = await self.accessor.get_unvoted_count(user)
        return (total_count, unvoted_count)
