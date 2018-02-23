#python imports
import os

#kiwi-surprise imports
import config

#surprise imports
from surprise import dump

def save_algorithm(algorithm):
    """
    Saves a trained algorithm to a file in the temp folder:
    <tempdir>/alg/trained_algorithm.data
    """
    create_file_if_not_existant()
    file_name = get_alg_persistence_filepath()
    dump.dump(file_name, algo=algorithm)

def load_algorithm():
    """
    Loads a trained algorithm from a file in the temp folder:
    <tempdir>/alg/trained_algorithm.data

    Returns None if not found
    """
    if not file_exists():
        return None
    file_name = get_alg_persistence_filepath()    
    _, loaded_algorithm = dump.load(file_name)
    return loaded_algorithm

def file_exists():
    return os.path.isfile(get_alg_persistence_filepath())

def create_file_if_not_existant():
    alg_temp_folder = get_alg_persistence_dir()
    if not os.path.exists(alg_temp_folder):
        os.makedirs(alg_temp_folder)

def get_alg_persistence_filepath():
    alg_temp_folder = get_alg_persistence_dir()
    return os.path.join(alg_temp_folder, "trained_algorithm.data")

def get_alg_persistence_dir():
    alg_temp_folder = os.path.join(config.temp_folder, "alg")
    return alg_temp_folder