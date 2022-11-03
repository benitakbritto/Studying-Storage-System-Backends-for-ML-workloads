import tiledb
import constants
import os
import shutil

if os.path.exists(constants.tileUri):
    shutil.rmtree(constants.tileUri)

tiledb.from_csv(
    constants.tileUri, 
    constants.dataset,
    names=['target','ids','date','flag','user','text']
    )