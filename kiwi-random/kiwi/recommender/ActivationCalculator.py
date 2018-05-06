from kiwi.database.DataAccessor import DataAccessor

import numpy
import math


class ActivationCalculator:
    def __init__(self, heuristics, data_accessor: DataAccessor):
        self.heuristics = heuristics
        self.accessor = data_accessor

    def exp_func(self, x):
        '''
        x is the number of votes the user has given
        '''
        return math.exp(-0.5 * x)*100

    async def get_activation(self):
        user = self.heuristics["user"]
        voted_count, _ = await self.accessor.get_voted_and_unvoted_count(user)
        a = self.exp_func(voted_count)
        print("Kiwi-Random Activation: {}".format(a))
        return a
