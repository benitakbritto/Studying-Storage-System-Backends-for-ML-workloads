import argparse
from tiledb.TileDBIterableDataset import TileDBIterableDataset
from torch.utils.data import DataLoader
from tiledb.db_util import get_dataset_count
from rocksDB.store import RocksDBStore

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
parser.add_argument("-input-file",
    help="Path to the input file stored in the filesystem",
    required=True)
parser.add_argument("-input-rows-per-key",
    help="Storing a batch of input rows under a single key",
    required=False)
 
# Read arguments from command line
args = parser.parse_args()

dataset = None
dataloader = None

if args.ds == 'rd':
    # Example: python main.py -ds rd -input-file /mnt/data/dataset/twitter/twitter_sentiment_dataset.csv -input-rows-per-key 256
    # Store data in rocks db
    store = RocksDBStore(args.input_file, args.input_rows_per_key)
    store.store_data()
    store.cleanup()

    # Invoke Dataloader
    
elif args.ds == 'td':
    dataset = TileDBIterableDataset(cache_len=args.pf, start=0, end=get_dataset_count())
    dataloader = DataLoader(dataset=dataset)
else:
    raise NotImplementedError("Not implemented")

for batch_idx, data in enumerate(dataloader):
    if batch_idx > 10: 
        break

    print(data)






