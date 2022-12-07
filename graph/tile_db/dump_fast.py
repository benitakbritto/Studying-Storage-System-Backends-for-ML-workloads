import tiledb

def dump_to_db(dataset_uri, tile_uri):
    tiledb.from_csv(
        tile_uri, 
        dataset_uri,
        names=['head','edge','tail'],
        sep='\t'
        )