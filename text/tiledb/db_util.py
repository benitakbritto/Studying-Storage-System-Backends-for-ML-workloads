import tiledb
from . import constants
import os
import shutil

def dump_to_db():
    if os.path.exists(constants.tileUri):
        shutil.rmtree(constants.tileUri)

    tiledb.from_csv(
        constants.tileUri, 
        constants.dataset,
        names=['target','ids','date','flag','user','text']
        )

def get_dataset_count():
    with tiledb.open(constants.tileUri, 'r') as A:
        return len(A)

if __name__ == "__main__":
    dump_to_db()

    print(get_dataset_count())
