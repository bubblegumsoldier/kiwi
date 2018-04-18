

class Recommender:
    def __init__(self, algorithm, data_accessor):
        self._algo = algorithm
        self._accessor = data_accessor

    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        voted, unvoted = await self._accessor.get_voted_and_unvoted_count(user)
        items = await self._accessor.get_unvoted_items(user)
        recommendations = await self._algo.get_top_n_items(user, items, count)

        return {
            'posts': [r[0] for r in recommendations],
            'user': user,
            'unvoted': unvoted,
            'voted': voted,
            'meta': [{'user': r[0], 'item': r[1], 'prediction': r[4], 'details': r[5]} for r in recommendations]
        }

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        success = await self._accessor.store_feedback(vote)
        voted, unvoted = await self._accessor \
            .get_voted_and_unvoted_count(vote.user)
        if success:
            return {
                'user': vote.user,
                'post': vote.post,
                'unvoted': unvoted,
                'voted': voted}
        return {}

    async def add_content(self, posts):
        filtered_posts = [post['id'] for post in posts]
        inserted = await self._accessor.add_content(filtered_posts)
        return {'inserted_count': inserted}

    async def predict_for(self, user, item):
        await self._register_user(user)
        prediction = await self._algo.predict(user, item)
        voted, unvoted = await self._accessor \
            .get_voted_and_unvoted_count(user)

        return {
            'user': user,
            'post': item,
            'voted': voted,
            'unvoted': unvoted,
            'prediction': prediction[3],
            'details': prediction[4]
        }

    async def _register_user(self, user):
        await self._accessor.register_user(user)
