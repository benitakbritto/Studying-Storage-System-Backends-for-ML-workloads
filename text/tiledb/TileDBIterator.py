import tiledb
import tiledb.constants  as constants
class TileDBIterator():
    def __init__(self, cache_len, start, end):
        # cache stores
        self.target = []
        self.text = []

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
            with tiledb.open(constants.tileUri, 'r') as A:
                # find last index to fetch(exclusive)
                self.last_exclusive_idx = min(self.curr_idx + self.cache_len, self.end_idx)

                # bulk fetch
                data = A.query(attrs=("target", "text"), coords=False, order='G')[self.curr_idx: self.last_exclusive_idx]
                
                # cache store
                self.target = data['target']
                self.text = data['text']
                
        # find the relative index within cache data
        relative_idx = self.curr_idx % len(self.target)
        
        # advance to next index
        self.curr_idx = self.curr_idx + 1

        return self.target[relative_idx], self.text[relative_idx]
