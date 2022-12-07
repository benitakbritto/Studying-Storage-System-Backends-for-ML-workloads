import math
from tile_db.TileDBIterator import TileDBIterator
from torch.utils.data import IterableDataset, get_worker_info

'''
Usage:  
ds = TileDBIterableDataset(start=0, end=1000, cache_len=100)
dl = DataLoader(ds, num_workers=0)
'''
class TileDBIterableDataset(IterableDataset):
    def __init__(self, start, end, cache_len, tile_uri):
        # assert end > start, "this example code only works with end > start"
        self.start = start
        self.end = end
        self.cache_len = cache_len
        self.tile_uri = tile_uri

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
        return TileDBIterator(cache_len=self.cache_len, start = iter_start, end = iter_end, tile_uri=self.tile_uri)
