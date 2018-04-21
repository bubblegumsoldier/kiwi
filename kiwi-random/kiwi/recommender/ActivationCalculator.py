from kiwi.database.DataAccessor import DataAccessor

import numpy
import math

class ActivationCalculator:
    def __init__(self, heuristics, data_accessor: DataAccessor):
        self.heuristics = heuristics
        self.accessor = data_accessor
    
    def g(self, x):
        return math.exp(-3.0*x)*100.0

    def f(self, x):
        v = numpy.random.exponential(1, None)/10.0
        v2 = 1 - v
        x = 1 - x
        gesamt = (((1-x)*v)+(((x**2)*(v2**2))**5))*50.0
        return gesamt

    async def get_activation(self):
        #needed heuristics:
        # user-votes in %
        # for this we need "user"
        MAX = 100

        user = self.heuristics["user"]
        voted_count, unvoted_count = await self.accessor.get_voted_and_unvoted_count(user)
        user_vote_ratio = float(voted_count) / float(voted_count + unvoted_count)

        a = min(MAX, 2*self.f(user_vote_ratio) + 0.8*self.g(user_vote_ratio))
        print("Kiwi-Random Activation: {}".format(a))
        return a