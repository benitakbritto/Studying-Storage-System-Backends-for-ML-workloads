import time
import numpy as np
import argparse
from data_gen import gen
from EmbedddingIterableDataset import EmbedddingIterableDataset
from torch.utils.data import DataLoader
from rocksdb_store import RocksDBEmbedding
from tiledb_store import TileDBEmbedding
from BaseStore import BaseStore

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-ds-size",
    help="Dataset size",
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

# r_store = RocksDBEmbedding()
# tile_store = TileDBEmbedding(rows_count=max_number, cols_count=emb_size, tile_uri=get_tile_uri(type))

ds_list = ['rd', 'td', 'ts']

for ds in ds_list:
    store = BaseStore()

    if ds == 'rd':
        store = RocksDBEmbedding()
    elif ds == 'td':
        store = TileDBEmbedding(rows_count=max_number + 1, cols_count=emb_size, tile_uri=get_tile_uri(type))
    elif ds == 'ts':
        pass
    else:
        NotImplementedError("unsupported datastore")

    start = time.time()

    for keys in dataloader:
        # convert to numpy
        keys = keys.numpy(force=False).tolist()

        # fetch the existing embs
        store.get_data(keys)
        # if ds == 'rd':
        #     last_emb = r_store.get_data(keys)
        # elif ds == 'td':
        #     last_emb = tile_store.get_data(keys)
        # elif ds == 'ts':
        #     pass
        # else:
        #     NotImplementedError("unsupported datastore")

        # create new embs
        new_embs = [gen_emb(emb_size) for _ in range(0, len(keys))]

        # write new embedding to store
        store.store_data(key_list=keys, value_list=new_embs)
        # if ds == 'rd':
        #     r_store.store_data(key_list=keys, value_list=new_embs)
        # elif ds == 'td':
        #     tile_store.store_data(key_list=keys, value_list=new_embs)
        # elif ds == 'ts':
        #     pass
        # else:
        #     NotImplementedError("unsupported datastore")

    end = time.time()

    print(f'Datastore: {ds}, Total time: {end-start} s')

