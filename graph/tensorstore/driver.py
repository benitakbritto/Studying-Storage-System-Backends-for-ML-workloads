from torch.utils.data import DataLoader, IterableDataset, get_worker_info
import time
from TensorStoreIterableDataset import TensorStoreIterableDataset
from db import TensorStoreDB
from dump_fast import TensorStoreDataset
import constants
import asyncio

'''
    Driver
'''

dbInstance = TensorStoreDB().db
dataset = TensorStoreDataset(dbInstance)

# Ingest data
loop = asyncio.get_event_loop()
start = time.time()

tasks = [
    loop.create_task(dataset.ingestData())
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
end = time.time()
print(f'Elapsed time in ingestion = {end - start}')

startKey = 
print(dbInstance.read(0,2).result())

# should give same set of data as range(3, 7), i.e., [3, 4, 5, 6].
# ds = TensorStoreIterableDataset(start=0, end=5, cache_len=1, db=dbInstance)

# start = time.time()
# run one at a time, too many tensor workers are causing issue

# Single-process loading
# output = list(DataLoader(ds, num_workers=8))
# sleep(3)

# # Mult-process loading with two worker processes
# # Worker 0 fetched [3, 4].  Worker 1 fetched [5, 6].
# output = list(DataLoader(ds, num_workers=2))
# sleep(3)

# # With even more workers
# output = DataLoader(ds, batch_size = 1024, num_workers = 8)
# read = 0

# for tensor in output:
#     read += tensor.shape[0]

# end = time.time()

# print(f'Elapsed time = {end - start}')
# print(f'Items read = {read}')