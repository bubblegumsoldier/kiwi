import os
from surprise import KNNWithMeans

def create_algorithm():
    """
    See: http://surprise.readthedocs.io/en/stable/prediction_algorithms.html
    """
    # sim_options = {
    #     'name': 'cosine',
    #     'user_based': False
    # }
    algo = KNNWithMeans(min_k=0, k=40,sim_options={'user_based': False})
    return algo

_dir_path = os.path.dirname(os.path.realpath(__file__))

temp_folder = os.path.join(_dir_path, ".temp")