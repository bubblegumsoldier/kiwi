import pandas as pd

def get_products():
    print("Loading products...")
    data_path = "/home/henry/Desktop/ml-latest-small/movies.csv"
    frame = pd.read_csv(data_path, sep=',', names=['id', 'title', 'tags_raw'])
    matrix = []
    for i, row in frame.iterrows():
        matrix.append(
            (row[0], row[2].split("|"))
        )
    print("Successfully loaded {} products".format(len(matrix)))
    return matrix