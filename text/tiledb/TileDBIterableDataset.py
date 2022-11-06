import math
from time import sleep
from tiledb.TileDBIterator import TileDBIterator
from torch.utils.data import IterableDataset, DataLoader, get_worker_info

'''
Usage:  
ds = TileDBIterableDataset(start=0, end=1000, cache_len=100)
dl = DataLoader(ds, num_workers=0)
'''
class TileDBIterableDataset(IterableDataset):
    def __init__(self, start, end, cache_len):
        # assert end > start, "this example code only works with end > start"
        self.start = start
        self.end = end
        self.cache_len = cache_len

        # with tiledb.open(constants.tileUri, 'r') as A:
        #     self.len = len(A)

    def __iter__(self):
        worker_info = get_worker_info()
        if worker_info is None:  # single-process data loading, return the full iterator
            iter_start = self.start
            iter_end = self.end
        else:  # in a worker process
            # split workload
            per_worker = int(math.ceil((self.end - self.start) / float(worker_info.num_workers)))
            worker_id = worker_info.id
            iter_start = self.start + worker_id * per_worker
            iter_end = min(iter_start + per_worker, self.end)
        return TileDBIterator(cache_len=self.cache_len, start = iter_start, end = iter_end)


if __name__ == "__main__":
    # should give same set of data as range(3, 7), i.e., [3, 4, 5, 6].
    ds = TileDBIterableDataset(start=3, end=7, cache_len=100)
    
    # run one at a time, too many tensor workers are causing issue

    # Single-process loading
    # print(list(DataLoader(ds, num_workers=0)))
    # sleep(3)

    # # Mult-process loading with two worker processes
    # # Worker 0 fetched [3, 4].  Worker 1 fetched [5, 6].
    # print(list(DataLoader(ds, num_workers=2)))
    # sleep(3)

    # With even more workers
    print(list(DataLoader(ds, num_workers=12)))
    sleep(3)
