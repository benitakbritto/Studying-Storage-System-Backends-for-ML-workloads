import argparse
import time
from tiledb.TileDBIterableDataset import TileDBIterableDataset
from torch.utils.data import DataLoader
from tiledb.db_util import get_dataset_count
from rocksDB.store import RocksDBStore
from rocksDB.map_style_data_loader import RocksDBMapStyleDataset

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
parser.add_argument("-type", 
    help = "Type of dataloader. m for map style and i for iterable style.", 
    choices=['m', 'i'],
    required=True)
parser.add_argument("-num-workers",
    help="Number of workers",
    default=0,
    required=False)
 
# Read arguments from command line
args = parser.parse_args()

dataset = None
dataloader = None

if args.ds == 'rd':
    # Example: python main.py -ds rd -input-file /mnt/data/dataset/twitter/twitter_sentiment_dataset.csv -input-rows-per-key 256 -type m
    # Store data in rocks db
    start = time.time()

    store = RocksDBStore(args.input_file, args.input_rows_per_key)
    store.store_data()
    store.store_metadata()
    
    end = time.time()

    print(f'{args.ds} Store time = {end - start} s')

    # Set Dataloader
    if args.type == 'm':
        dataset = RocksDBMapStyleDataset()
        dataloader = DataLoader(
            dataset,
            batch_size=dataset.rows_in_key,
            shuffle=False, 
            num_workers=args.num_workers
        )
    elif args.type == 'i':
        total_rows = store.get_total_input_rows()
        dataset = TileDBIterableDataset(cache_len=int(args.pf), start=0, end=int(total_rows))
        dataloader = DataLoader(dataset=dataset)
    
    store.cleanup()
    
elif args.ds == 'td':
    dataset = TileDBIterableDataset(cache_len=args.pf, start=0, end=get_dataset_count())
    dataloader = DataLoader(dataset=dataset)
else:
    raise NotImplementedError("Not implemented")

# Call dataloader
start = time.time()

for batch_idx, data in enumerate(dataloader):
    i = batch_idx

end = time.time()
print(f'{args.ds} Dataloader time = {end - start} s')






