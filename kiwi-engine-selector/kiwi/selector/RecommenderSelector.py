from kiwi.selector.Recommender import Recommender
import kiwi.selector.recommender_distribution as distribution
from kiwi.selector.HeuristicFetcher import HeuristicFetcher
from logging import getLogger


class RecommenderSelector:
    def __init__(self, recommenders):
        self.recommenders = recommenders
        self.decisions = {}

    @classmethod
    def from_config(cls, config):
        recommenders = {}
        for label, config in config.items():
            recommenders[label] = Recommender.from_config(config)
        return cls(recommenders)

    async def get_recommendations(self, session, request):
        recommender, name = await \
            self.choose_recommenders(session, request.user)
        items = await recommender.get_content_for_user(session, request)
        items.json['recommender'] = name
        return items

    async def predict_for(self, session, user, item):
        recommender, name = await self.choose_recommenders(session, user)
        return await recommender.predict_for(session, user, item)

    async def get_heuristics(self, params):
        # don't know how to make sure that we avoid collision, that's why I will just reinstatiate the HeuristicFetcher
        heuristic_fetcher = HeuristicFetcher()
        heuristic_fetcher.update(params)
        all_heuristics = heuristic_fetcher.get_heuristics()
        return all_heuristics

    async def choose_recommenders(self, session, user):
        highest_recommender = None
        highest_activation = -1000
        for recommender in self.recommenders:
            # not all recommenders will get the exact same heuristics...
            # (e.g. time and age may vary during the iteration... - but for now that's okay)
            params = {
                'user': user,
                'algorithm': recommender
            }
            heuristics = await self.get_heuristics(params)

            activation = await self.recommenders[recommender].get_activation(session, heuristics)
            getLogger("info").info(
                "Recommender {} has an activation of {}".format(recommender, activation))
            if activation > highest_activation:
                highest_activation = activation
                highest_recommender = recommender

        getLogger("info").info("Highest recommender is {} with an actication value of {}".format(
            highest_recommender, highest_activation))
        print("Highest recommender is {} with an actication value of {}".format(
            highest_recommender, highest_activation))
        await self._log_selection(highest_recommender)
        return self.recommenders[highest_recommender], highest_recommender

    async def _log_selection(self, r):
        if r in self.decisions:
            self.decisions[r] += 1
        else:
            self.decisions[r] = 1

    async def distribute_posts(self, session, posts):
        return await distribution.content(session, self.recommenders, posts)

    async def distribute_vote(self, session, vote):
        return await distribution.feedback(session, self.recommenders, vote)

    async def distribute_votes(self, session, votes):
        return await distribution.votes(session, self.recommenders, votes)
