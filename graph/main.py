import argparse
import asyncio
from pathlib import Path
from tile_db.TileDBIterableDataset import TileDBIterableDataset
from tile_db.TileDBMapDataset import TileDBMapDataset
import time, os, shutil
from torch.utils.data import DataLoader
import tile_db.dump_fast as tile_db_dump
from tile_db.helper import get_dataset_count
from rocksDB.store import RocksDBStore
from rocksDB.map_style_data_loader import RocksDBMapStyleDataset
from rocksDB.iterable_style_data_loader import RocksDBIterableDataset
from tensor_store.store import TSStore
from tensor_store.TensorStoreDataset import TensorStoreDataset
import rocksDB.db_util
from baseline_iterable import BaselineGraphIterableDataset

# Initialize parser
parser = argparse.ArgumentParser()

# Adding  argument
parser.add_argument("-ds", 
    help = "Backend Data Store. rd for RocksDB, ts for TensorStore, td for TileDB", 
    choices=['rd', 'ts', 'td', 'base'],
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
parser.add_argument("-skip-write",
    help="Skip write to data store",
    default=False,
    required=False)

# Read arguments from command line
args = parser.parse_args()

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
            if not args.skip_write:
                rocksDB.db_util.delete_db()
                start = time.time()

                store = RocksDBStore(args.input_file, int(args.input_rows_per_key))
                store.store_data()
                store.store_metadata()
                
                end = time.time()

                store.cleanup()

            # Set Dataloader
            if args.type == 'm':
                dataset = RocksDBMapStyleDataset()
                dataloader = DataLoader(
                    dataset,
                    batch_size=int(args.batch_size),
                    num_workers=int(args.num_workers)
                )

            elif args.type == 'i':
                total_rows = rocksDB.db_util.get_total_input_rows()
                dataset = RocksDBIterableDataset(cache_len=int(args.pf), start=0, end=int(total_rows))
                dataloader = DataLoader(dataset=dataset, 
                    num_workers=int(args.num_workers), 
                    batch_size=int(args.batch_size))

        elif args.ds == 'td':
            # dump to db
            root_dir = str(Path(args.input_file).parent)

            # switch to input file name from args
            dataset_uri = args.input_file
            tile_uri = root_dir + "/fb15k-237.tldb"

            if not args.skip_write:
                # destroy path
                if os.path.exists(tile_uri):
                    shutil.rmtree(tile_uri)
                    
                start = time.time()
                tile_db_dump.dump_to_db(tile_uri=tile_uri, dataset_uri=dataset_uri)
                end = time.time()

            # hardcoded as finding len programmatically causes workers freeze for some reason
            size = 272115

            # prepare dataset and dataloader
            if args.type == 'i':
                dataset = TileDBIterableDataset(cache_len=int(args.pf), start=0, end=size, tile_uri=tile_uri)
            elif args.type == 'm':
                dataset = TileDBMapDataset(size=size, tile_uri=tile_uri)

            dataloader = DataLoader(dataset=dataset, batch_size=int(args.batch_size), num_workers=int(args.num_workers))

        elif args.ds == 'ts':            
            store = TSStore(args.input_file)
            
            # Ingest data
            loop = asyncio.get_event_loop()

            if not args.skip_write:
                os.system('sudo rm -rf /mnt/data/store')
                start = time.time()
                # task = [loop.create_task(store.ingestData())]
                store.ingestData()
                # loop.run_until_complete(asyncio.wait(task)) 
                # loop.close()

                end = time.time()

            # Set Dataloader
            if args.type == 'm':
                dataset = TensorStoreDataset(store.db)
                dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    num_workers=int(args.num_workers)
                )
            elif args.type == 'i':
                raise NotImplementedError("Not implemented")

        elif args.ds == 'base':
            if args.type == 'i':
                dataset = BaselineGraphIterableDataset(args.input_file)
            else:
                raise NotImplementedError("Not implemented")

            dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    shuffle=False,
                    num_workers=0)
        
        else:
            raise NotImplementedError("Not implemented")


        if not args.skip_write and args.ds!='base':
            print(f'{args.ds} Write = {end - start} s')

        # Call dataloader
        start = time.time()

        for batch_idx, data in enumerate(dataloader):
            i = batch_idx

        end = time.time()
        print(f'{args.ds} Dataloader time = {end - start} s')


if __name__ == "__main__":
    run_test()
        
