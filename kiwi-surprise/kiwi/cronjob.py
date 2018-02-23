# import the persistence module (database_loader.py)
# take the mysql-data and serialize it to .csv
# train an algorithm with the given data-set
# save the algorithm to the temp file (algorithm_persistence_tools.py)
# Format (ref http://surprise.readthedocs.io/en/stable/reader.html#surprise.reader.Reader):
#
# user ; item ; rating ; [timestamp]
#
# should look something like
# reader = Reader(line_format='user ; item ; rating ; timestamp', sep=';')
#
# save the data to a temp file

def main():
    pass