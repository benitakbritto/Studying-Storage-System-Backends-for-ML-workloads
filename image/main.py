import argparse
from tile_db.TileDBIterableDataset import TileDBIterableDataset
from tile_db.TileDBMapDataset import TileDBMapDataset
import time, os, shutil
from tile_db.helper import get_dataset_count
import tile_db.dump_fast as tile_db_dump
from torch.utils.data import DataLoader
from rocksDB.store import RocksDBStore
from rocksDB.map_style_data_loader import RocksDBMapStyleDataset
from rocksDB.iterable_style_data_loader import RocksDBIterableDataset
from tensor_store.store import TSStore
from tensor_store.data_loader import TensorStoreDataset
from tensor_store.TensorStoreIterableDataset import TensorStoreIterableDataset
import rocksDB.db_util
from multiprocessing import Process


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
    default=1,
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
parser.add_argument("-batch-size",
    help="Batch size for the dataloader",
    default=256,
    required=False)
parser.add_argument("-itr",
    help="Number of iterations to run test",
    default=1,
    required=False)


# Read arguments from command line
args = parser.parse_args()

def ingest_to_ts(filename):
    store = TSStore(filename)
    store.ingest_data()

def run_test():
    print(f'ds = {args.ds} | \
        pf = {args.pf} | \
        input-file = {args.input_file} | \
        input-rows-per-key = {args.input_rows_per_key} | \
        type = {args.type} | \
        num-workers = {args.num_workers} | \
        batch-size = {args.batch_size} | \
        itr = {args.itr}')
    
    for i in range(int(args.itr)):
        print(f'Iteration {i + 1}')

        dataset = None
        dataloader = None
        start = None
        end = None

        if args.ds == 'rd':
            # Store data in rocks db
            start = time.time()

            store = RocksDBStore(args.input_file, int(args.input_rows_per_key))
            store.store_data()
            store.store_metadata()
            
            end = time.time()

            total_rows = store.get_total_input_rows()
            store.cleanup()

            # Set Dataloader
            if args.type == 'm':
                dataset = RocksDBMapStyleDataset()
                dataloader = DataLoader(
                    dataset,
                    batch_size=int(args.batch_size),
                    shuffle=False, 
                    num_workers=int(args.num_workers)
                )
            elif args.type == 'i':
                dataset = RocksDBIterableDataset(cache_len=int(args.pf), start=0, end=int(total_rows))
                dataloader = DataLoader(dataset=dataset, 
                    num_workers=int(args.num_workers), 
                    batch_size=int(args.batch_size))

        elif args.ds == 'td':
            # dump to db
            root_dir = args.input_file
            tile_uri = root_dir + "/cifar100.tldb"

            # destroy path
            if os.path.exists(tile_uri):
                shutil.rmtree(tile_uri)

            start = time.time()
            tile_db_dump.dump_to_db(root_dir=root_dir, tile_uri=tile_uri)
            end = time.time()

            # prepare dataset and dataloader
            if args.type == 'i':
                dataset = TileDBIterableDataset(cache_len=int(args.pf), start=0, end=get_dataset_count(tile_uri=tile_uri), tile_uri=tile_uri)
            elif args.type == 'm':
                dataset = TileDBMapDataset(size=get_dataset_count(), tile_uri=tile_uri)

            dataloader = DataLoader(dataset=dataset, batch_size=int(args.batch_size), num_workers=int(args.num_workers))

        elif args.ds == 'ts':
            start = time.time()
            ingest_process = Process(target=ingest_to_ts, args={args.input_file,})
            ingest_process.start()
            ingest_process.join()
            end = time.time()

            # Set Dataloader
            if args.type == 'i':
                #TODO get input size from args or constants
                dataset = TensorStoreIterableDataset(start=0, end=50000, cache_len=int(args.pf))
            elif args.type == 'm':
                dataset = TensorStoreDataset()
            else:
                raise NotImplementedError("Not implemented")
                
            dataloader = DataLoader(
                dataset,
                batch_size = int(args.batch_size), 
                shuffle=False, 
                num_workers=int(args.num_workers)
            )

        else:
            raise NotImplementedError("Not implemented")


        print(f'{args.ds} Write = {end - start} s')

        # Call dataloader
        start = time.time()

        for batch_idx, data in enumerate(dataloader):
            i = batch_idx

        end = time.time()
        print(f'{args.ds} Dataloader time = {end - start} s')


if __name__ == "__main__":
    run_test()

    # cleanup
    if args.ds == 'rd':
        rocksDB.db_util.delete_db()