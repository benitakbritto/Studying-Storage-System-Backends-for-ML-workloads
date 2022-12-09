import time
import numpy as np
import argparse
from data_gen import gen
from EmbedddingIterableDataset import EmbedddingIterableDataset
from torch.utils.data import DataLoader
from rocksDB.store import RocksDBEmbedding

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

parser.add_argument("-ds", 
    help = "Backend Data Store. rd for RocksDB, ts for TensorStore, td for TileDB", 
    choices=['rd', 'ts', 'td'],
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
ds = args.ds
type = args.type
input_file = args.input_file

# create dataset, fetch the max numbers which is required for TensorStore and TileDB
max_number = gen(type=type, size=ds_size, output_file=path)

dataset = EmbedddingIterableDataset(path=path)
dataloader = DataLoader(dataset, batch_size = batch_size)

r_store = RocksDBEmbedding()


def gen_emb(size):
    return np.random.random(size=size)

start = time.time()
for keys in dataloader:
    # convert to numpy
    keys = keys.numpy(force=False).tolist()

    # fetch the existing embs
    if ds == 'rd':
        last_emb = r_store.get_data(keys)
    elif ds == 'tdb':
        pass
    elif ds == 'ts':
        pass
    else:
        NotImplementedError("unsupported datastore")

    # create new embs
    new_embs = [gen_emb(emb_size) for _ in range(0, len(keys))]

    # write new embedding to store
    if ds == 'rd':
        r_store.store_data(key_list=keys, value_list=new_embs)
    elif ds == 'tdb':
        pass
    elif ds == 'ts':
        pass
    else:
        NotImplementedError("unsupported datastore")

end = time.time()

print(f'Total time: {end-start} s')