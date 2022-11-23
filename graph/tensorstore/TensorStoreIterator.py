import tensorstore as ts
import constants

class TensorStoreIterator():
    def __init__(self, cache_len, start, end, db):
        # cache stores
        self.tensors = []

        self.curr_idx = start
        self.end_idx = end
        # idx after which we need to fetch from DB
        self.last_exclusive_idx = start - 1
        
        # items to fetch in one shot, don't overfetch
        # import pdb; pdb.set_trace()
        self.cache_len = min(cache_len, end - start + 1)

        self.db = db

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_idx >= self.end_idx:
            raise StopIteration

        # pre-fetch
        elif self.curr_idx >= self.last_exclusive_idx:
            # print('fetching:', self.curr_idx)
            
            # find last index to fetch(exclusive)
            self.last_exclusive_idx = min(self.curr_idx + self.cache_len, self.end_idx)

            # bulk fetch
            data = self.db[self.curr_idx : self.last_exclusive_idx, : ].read().result()
            data_str = data.decode()
            # cache store
            self.tensors = data.decode()
                
        # find the relative index within cache data
        relative_idx = self.curr_idx % len(self.tensors)
        
        # advance to next index
        self.curr_idx = self.curr_idx + 1

        return self.tensors[relative_idx]
