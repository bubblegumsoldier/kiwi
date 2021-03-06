class Recommender:
    def __init__(self, algorithm, data_accessor, config):
        self._algo = algorithm
        self._accessor = data_accessor
        self._max_vote = config['max_rating']
        self._min_vote = config['min_rating']

    async def recommend_for(self, user, count=10):
        await self._register_user(user)
        voted_count, unvoted_count = await \
            self._accessor.get_voted_and_unvoted_count(user)
        unvoted = await self._accessor.get_unvoted_items(user)
        ranking = await self._algo.predict_similarities(user)

        choose = ranking[ranking['ItemId'].isin(unvoted)]
        returns = choose[:count]

        return {
            'posts': returns['ItemId'].tolist(),
            'user': user,
            'unvoted': unvoted_count,
            'voted': voted_count,
            'meta': [
                (self._scale_rating(rows[0]), rows[1])
                for i, rows in returns.iterrows()
            ]
        }

    async def store_feedback(self, vote):
        await self._register_user(vote.user)
        await self._algo.update_ratings(vote)
        await self._algo.build_user_taste_vector(vote.user, insert=True)
        success = await self._accessor.store_feedback(vote)
        if success:
            voted, unvoted = await self._accessor.get_voted_and_unvoted_count(vote.user)
            return {'user': vote.user, 'post': vote.post, 'unvoted': unvoted, 'voted': voted}
        return {}

    async def predict(self, user, item):
        await self._register_user(user)
        voted_count, unvoted_count = await \
            self._accessor.get_voted_and_unvoted_count(user)
        similarity = await self._algo.predict_similarities(user, item)
        
        return {
            'prediction': self._scale_rating(similarity['Similarities'][0]),
            'user': user,
            'post': item,
            'voted': voted_count,
            'unvoted': unvoted_count
        }

    async def _register_user(self, user):
        await self._accessor.register_user(user)

    def _scale_rating(self, similarity):
        positive_sim = 0.5*(similarity+1)
        return (1-positive_sim)*self._min_vote + positive_sim*self._max_vote