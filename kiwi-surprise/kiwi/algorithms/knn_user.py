import surprise


def create_algorithm():
    """
    See: http://surprise.readthedocs.io/en/stable/prediction_algorithms.html
    Just change the algorithm and the option set for a different prediction algorithm.
    """
    options = {
        'name': 'cosine',
        'user_based': True
    }
    algo = surprise.KNNWithMeans(
        min_k=1,
        k=40,
        sim_options=options)

    return algo



async def get_activation(heuristics, accessor):
    voted_count, unvoted_count = await accessor.get_voted_and_unvoted_count(heuristics["user"])
    u = float(voted_count) / float(voted_count + unvoted_count)
    import random
    return min(100, u*100 + random.randrange(10))
