import tiledb
import constants
import os
import shutil

def dump_to_db():
    if os.path.exists(constants.tileUri):
        shutil.rmtree(constants.tileUri)

    tiledb.from_csv(
        constants.tileUri, 
        constants.dataset,
        names=['head','edge','tail'],
        sep='\t'
        )

if __name__ == "__main__":
    dump_to_db()
    
    pass