import tiledb

def get_dataset_count(tile_uri):
    count = None
    with tiledb.open(tile_uri, 'r') as A:
        count = A.shape[0]
        A.close()
    
    # print("dataaset count:", count)
    return count