import time
import numpy as np
import argparse
from data_gen import gen
from EmbedddingIterableDataset import EmbedddingIterableDataset
from torch.utils.data import DataLoader
from rocksdb_store import RocksDBEmbedding
from tiledb_store import TileDBEmbedding
from ts_store import TSEmbedding
from BaseStore import BaseStore

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-ds-size",
    help="Dataset size",
    required=False)

parser.add_argument("-ds", 
    help = "Backend Data Store. rd for RocksDB, ts for TensorStore, td for TileDB. all for All", 
    choices=['rd', 'ts', 'td', 'all'],
    required=False)

parser.add_argument("-batch-size",
    help="Batch size",
    default=256,
    required=False)

parser.add_argument("-embed-size",
    help="Size of each embedding",
    default=100,
    required=False)

parser.add_argument("-input-file",
    help="Path to the input file",
    required=True)

parser.add_argument("-type", 
    help = "power for Graph. zipf for Text", 
    default='zipf',
    choices=['power', 'zipf'],
    required=False)

# Read arguments from command line
args = parser.parse_args()

# collect params
path = args.input_file
batch_size = int(args.batch_size)
ds_size = int(args.ds_size)
emb_size = int(args.embed_size)
type = args.type
input_file = args.input_file

# create dataset, fetch the max numbers which is required for TensorStore and TileDB
max_number = gen(type=type, size=ds_size, output_file=path)
print("dataset prepared")

dataset = EmbedddingIterableDataset(path=path)
dataloader = DataLoader(dataset, batch_size = batch_size)

def get_tile_uri(type):
    root = "/mnt/data/embeddings/"

    if type == 'power':
        return root + "power.tldb"
    else:
        return root + "zipf.tldb"

def gen_emb(size):
    return np.random.random(size=size)

def get_unique_kv(key_list, value_list):
    kv = dict()

    for i, key in enumerate(key_list):
        kv[key] = value_list[i]
    
    keys = []
    values = []

    for k, v in kv.items():
        keys.append(k)
        values.append(v)
    
    return keys, values

# r_store = RocksDBEmbedding()
# tile_store = TileDBEmbedding(rows_count=max_number, cols_count=emb_size, tile_uri=get_tile_uri(type))

ds_list = ['rd','td']

if args.ds != 'all':
    ds_list = [args.ds]

for ds in ds_list:
    store = BaseStore()

    if ds == 'rd':
        store = RocksDBEmbedding()
    elif ds == 'td':
        store = TileDBEmbedding(rows_count=max_number + 1, cols_count=emb_size, tile_uri=get_tile_uri(type))
    elif ds == 'ts':
        # dimensions must exactly match the rows_count, cols_count
        store = TSEmbedding(rows_count=max_number + 1, cols_count=emb_size)
    else:
        NotImplementedError("unsupported datastore")

    start = time.time()

    for keys in dataloader:
        # convert to numpy
        key_list = keys.numpy(force=False).tolist()

        # fetch the existing embs
        store.get_data(key_list=key_list)

        # create new embs
        new_embs = [gen_emb(emb_size) for _ in range(0, len(keys))]

        # there might be duplicate keys, so building unique kv pairs
        key_list, value_list = get_unique_kv(key_list=key_list, value_list=new_embs)

        # write new embedding to store
        store.store_data(key_list=key_list, value_list=value_list)
        
    end = time.time()

    print(f'Datastore: {ds}, Total time: {end-start} s')

