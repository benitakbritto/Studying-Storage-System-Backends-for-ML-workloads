import tiledb
import os
import shutil

def dump_to_db(dataset_uri, tile_uri):
    if os.path.exists(tile_uri):
        shutil.rmtree(tile_uri)

    tiledb.from_csv(
        tile_uri, 
        dataset_uri,
        names=['head','edge','tail'],
        sep='\t'
        )