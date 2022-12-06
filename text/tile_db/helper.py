import tiledb

def get_dataset_count(tile_uri):
    with tiledb.open(tile_uri, 'r') as A:
        return len(A)