from Algorithm import Algorithm


class Recommender:
    def __init__(self, algorithm: Algorithm, data_accessor):
        self._algo = algorithm
        self._accessor = data_accessor

    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        items = await self._accessor.get_unvoted_items(user)
        recommendations = await self._algo.get_top_n_items(user, items, count)
        unvoted = len(items)
        return {
            'posts': [r[0] for r in recommendations],
            'user': user,
            'unvoted': unvoted
        }

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        success = await self._accessor.store_feedback(vote)
        unvoted = await self._accessor.get_unvoted_count(vote.user)
        if success:
            return {'user': vote.user, 'post': vote.post, 'unvoted': unvoted}
        return {}

    async def add_content(self, posts):
        filtered_posts = [post['id'] for post in posts]
        inserted = await self._accessor.add_content(filtered_posts)
        return {'inserted_count': inserted}

    async def _register_user(self, user):
        await self._accessor.check_and_register_user(user)
