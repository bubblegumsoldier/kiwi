import random
import surprise
import math


def sigmoid(x, shift, scale):
    return 1 / (1 + math.exp(scale * x + shift))


def create_algorithm():
    """
    See: http://surprise.readthedocs.io/en/stable/prediction_algorithms.html
    Just change the algorithm and the option set for a different prediction algorithm.
    """
    algo = surprise.prediction_algorithms.matrix_factorization.SVD()

    return algo


async def get_activation(heuristics, accessor, predictor):
    voted_count, _ = await accessor.get_voted_and_unvoted_count(heuristics["user"])
    total_ratings = await predictor.get_rating_count()
    total_users = await accessor.count_users()
    total_items = await accessor.count_items()
    try:
        rd = total_ratings / (total_items * total_users)
    except ZeroDivisionError:
        rd = 0

    return sigmoid(voted_count, 5, -0.5) * 50 + sigmoid(total_ratings * rd, 3, -0.5) * 30
