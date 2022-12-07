import tiledb
import numpy as np

class TileDBIterator():
    def __init__(self, cache_len, start, end, tile_uri):
        self.tile_uri = tile_uri
        # cache stores
        self.label = []
        self.im = []

        self.curr_idx = start
        self.end_idx = end
        # idx after which we need to fetch from DB
        self.last_exclusive_idx = start - 1
        
        # items to fetch in one shot, don't overfetch
        # import pdb; pdb.set_trace()
        self.cache_len = min(cache_len, end - start + 1)

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_idx >= self.end_idx:
            print('raising ex:', self.curr_idx)
            raise StopIteration

        # pre-fetch
        elif self.curr_idx >= self.last_exclusive_idx:
            # print('fetching:', self.curr_idx)
            with tiledb.open(self.tile_uri, 'r') as A:
                # find last index to fetch(exclusive)
                self.last_exclusive_idx = min(self.curr_idx + self.cache_len, self.end_idx)

                # bulk fetch
                data = A.query(attrs=("im", "label"), coords=False, order='G')[self.curr_idx: self.last_exclusive_idx]

                # cache store
                self.im = data['im']
                # we stored as tuple, now transform back to array
                self.im = np.array([list(t) for t in self.im])
                
                # import pdb; pdb.set_trace()
                self.label = data['label']
                
        # find the relative index within cache data
        relative_idx = self.curr_idx % len(self.label)
        
        # advance to next index
        self.curr_idx = self.curr_idx + 1

        return self.label[relative_idx], self.im[relative_idx]
