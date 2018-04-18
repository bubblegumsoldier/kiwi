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



def get_activation(heuristics):
    return 0
