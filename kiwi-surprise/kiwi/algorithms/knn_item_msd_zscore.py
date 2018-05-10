import surprise
from kiwi.algorithms.utils import sigmoid


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


async def get_activation(heuristics, accessor, predictor):
    voted_count, _ = await accessor.get_voted_and_unvoted_count(heuristics["user"])
    total_users = await accessor.count_users()
    global_rating_mean = await accessor.average_rating_count()
    try:
        rd = global_rating_mean / total_users
    except ZeroDivisionError:
        rd = 0

    return (sigmoid(voted_count, 5, -0.5) * 30 +
            sigmoid(rd, 10, -100) * 50)
