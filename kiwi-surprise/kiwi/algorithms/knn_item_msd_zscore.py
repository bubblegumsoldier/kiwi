import surprise
from random import randrange


def create_algorithm():
    """
    See: http://surprise.readthedocs.io/en/stable/prediction_algorithms.html
    Just change the algorithm and the option set for a different prediction algorithm.
    """
    options = {
        'name': 'msd',
        'user_based': False
    }
    algo = surprise.KNNWithZScore(
        min_k=1,
        k=40,
        sim_options=options)

    return algo


async def get_activation(heuristics, accessor):
    voted_count, unvoted_count = await accessor.get_voted_and_unvoted_count(heuristics["user"])
    try:
        u = float(voted_count) / float(voted_count + unvoted_count)
    except ZeroDivisionError:
        u = 0
    return min(100, u * 100 + randrange(10))
