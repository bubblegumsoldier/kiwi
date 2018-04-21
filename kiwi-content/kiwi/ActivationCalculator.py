from kiwi.database.DataAccessor import DataAccessor

import numpy
import math

class ActivationCalculator:
    def __init__(self, heuristics, accessor):
        self.heuristics = heuristics
        self.accessor = accessor
    
    async def get_activation(self, user_taste_vector):
        #needed heuristics:
        # user-votes in %
        # for this we need "user"
        if user_taste_vector is None:
            return 0
        
        utv = user_taste_vector

        MAX = 100

        user = self.heuristics["user"]
        
        voted_count, unvoted_count = await self.accessor.get_voted_and_unvoted_count(user)
        u = float(voted_count) / float(voted_count + unvoted_count)

        v = numpy.std(utv) / numpy.mean(utv)
        print("Deviation: {}".format(v))
        f = math.exp((-(100.0/9.0)*(u**2))+((100.0/9.0)*u)) * 6 * v
        a = min(MAX, f)

        return a