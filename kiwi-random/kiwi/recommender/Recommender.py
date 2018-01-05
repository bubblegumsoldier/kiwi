
class Recommender:
    def __init__(self, data_accessor):
        self.accessor = data_accessor

    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        return await self.accessor.recommend_for(user, count)

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
