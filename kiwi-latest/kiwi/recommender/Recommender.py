from kiwi.database.DataAccessor import DataAccessor


class Recommender:
    def __init__(self, data_accessor: DataAccessor, min_rating=0, max_rating=1):
        self.accessor = data_accessor
        self.min = min_rating
        self.max = max_rating

    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        recommendations = await self.accessor.recommend_for(user, count)
        voted_count, total_count = await self.accessor \
            .get_voted_and_total_count(user)
        return {
            'user': user,
            'recommendations': recommendations,
            'unvoted': total_count - voted_count,
            'voted': voted_count
        }

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        success = await self.accessor.store_feedback(vote)
        voted_count, total_count = await self.accessor \
            .get_voted_and_total_count(vote.user)
        if success:
            return {
                'user': vote.user,
                'post': vote.post,
                'unvoted': total_count - voted_count,
                'voted': voted_count}
        return {}

    async def add_content(self, posts):
        inserted = await self.accessor.add_content(post['id'] for post in posts)
        return {'inserted_count': inserted}

    async def predict_for(self, user, item):
        await self._register_user(user)
        voted_count, total_count = await self.accessor \
            .get_voted_and_total_count(user)
        ranking = await self.accessor.get_ranking(item)

        prediction = max(
            [self.max * (1 - ranking / total_count), self.min])
        return {
            'prediction': prediction,
            'user': user,
            'post': item,
            'voted': voted_count,
            'unvoted': total_count - voted_count
        }

    async def store_votes(self, votes):
        await self.accessor.insert_votes(votes)

    async def _register_user(self, user):
        await self.accessor.register_user(user)
