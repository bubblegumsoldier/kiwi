import pandas as pd
import os

def get_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Loading data...")
    data_path = os.path.join(dir_path, "data", "votes_formatted.csv")
    frame = pd.read_csv(data_path, sep=';', names=['UserId', 'ItemId', 'Vote'])
    matrix = []
    for i, row in frame.iterrows():
        matrix.append(tuple(row.tolist()[:2]))
    print("Successfully loaded {} ratings".format(len(matrix)))
    return matrix