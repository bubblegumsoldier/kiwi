import pandas as pd
import os

def get_products():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Loading products...")
    data_path = os.path.join(dir_path, "data", "upic_posts.csv")
    frame = pd.read_csv(data_path, sep=',', names=['id', 'tags_raw'])
    matrix = []
    for i, row in frame.iterrows():
        matrix.append(
            (row[0], row[1].split("|"))
        )
    print("Successfully loaded {} products".format(len(matrix)))
    return matrix