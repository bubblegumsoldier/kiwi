import pandas as pd

def get_data():
    print("Loading data...")
    data_path = "/home/henry/Desktop/ml-latest-small/ratings.csv"
    frame = pd.read_csv(data_path, sep=',', names=['UserId', 'ItemId', 'Vote', 'Time'])
    matrix = []
    for i, row in frame.iterrows():
        matrix.append(tuple(row.tolist()[:3]))
    print("Successfully loaded {} ratings".format(len(matrix)))
    return matrix