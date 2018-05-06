import pandas as pd
import os

def get_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Loading data...")
    data_path = os.path.join(dir_path, "data", "ratings.dat")
    frame = pd.read_csv(data_path, sep=':', names=['UserId', 'ItemId', 'Vote', 'Time'])
    matrix = []
    for i, row in frame.iterrows():
        items_as_list = row.tolist()[:3]
        items_as_list_as_int = [int(item) for item in items_as_list]
        matrix.append(tuple(items_as_list_as_int))
    print("Successfully loaded {} ratings".format(len(matrix)))
    return matrix