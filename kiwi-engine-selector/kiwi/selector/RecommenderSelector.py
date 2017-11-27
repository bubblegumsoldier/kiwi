from kiwi.selector.Recommender import Recommender
import kiwi.selector.recommender_distribution as distribution


class RecommenderSelector:
    def __init__(self, recommenders):
        self.recommenders = recommenders

    @classmethod
    def from_config(cls, config):
        recommenders = {}
        for label, config in config.items():
            recommenders[label] = Recommender.from_config(config)
        return cls(recommenders)

    async def get_pictures(self, session, user):
        recommender = await self.choose_recommenders(user)
        pics = await recommender.get_pics_for_user(session, user)
        return pics

    async def choose_recommenders(self, user):
        # todo
        return self.recommenders['random']

    async def distribute_posts(self, session, posts):
        return await distribution.content(session, self.recommenders, posts)

    async def distribute_vote(self, session, vote):
        return await distribution.feedback(session, self.recommenders, vote)
