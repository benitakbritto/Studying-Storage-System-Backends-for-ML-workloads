import argparse
from tile_db.TileDBIterableDataset import TileDBIterableDataset
from torch.utils.data import DataLoader
from tile_db.helper import get_dataset_count
import tile_db.dump as tile_db_dump

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding  argument
parser.add_argument("-ds", 
help = "Backend Data Store. rd for RocksDB, ts for TensorStore, td for TileDB", 
choices=['rd', 'ts', 'td'],
required=True)

parser.add_argument("-pf",
help="Number of items to prefetch within dataset",
default=1,
required=False)
 
# Read arguments from command line
args = parser.parse_args()

dataset = None
dataloader = None

if args.ds == 'rd':
    raise NotImplementedError("Not implemented")
elif args.ds == 'td':
    # dump to db
    rootDir = "/mnt/data/dataset/twitter/"

    # switch to input file name from args
    dataset_uri = rootDir + "twitter_sentiment_dataset.csv"
    tile_uri = rootDir + "twitter.tldb"

    tile_db_dump.dump_to_db(tile_uri=tile_uri, dataset_uri=dataset_uri)

    # prepare dataset and dataloader
    dataset = TileDBIterableDataset(cache_len=int(args.pf), start=0, end=get_dataset_count(tile_uri=tile_uri), tile_uri=tile_uri)
    dataloader = DataLoader(dataset=dataset)
else:
    raise NotImplementedError("Not implemented")

for batch_idx, data in enumerate(dataloader):
    if batch_idx > 10: 
        break

    print(data)






