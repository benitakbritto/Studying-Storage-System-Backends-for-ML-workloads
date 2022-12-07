from rocksdict import Rdict
import rocksDB.constants
import rocksDB.helper as bytes
import io
import torch

class RocksDBIterator():
    def __init__(self, cache_len, start, end):
        self.db = Rdict(rocksDB.constants.DB_PATH)

        # cache stores
        self.image_with_label = []

        self.curr_idx = start
        self.end_idx = end

        # idx after which we need to fetch from DB
        self.last_exclusive_idx = start - 1
        
        # items to fetch in one shot, don't overfetch
        self.cache_len = min(cache_len, end - start + 1)

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_idx >= self.end_idx:
            print('raising ex:', self.curr_idx)
            raise StopIteration

        # pre-fetch
        elif self.curr_idx >= self.last_exclusive_idx:
            # find last index to fetch(exclusive)
            self.last_exclusive_idx = min(self.curr_idx + self.cache_len, self.end_idx)

            # bulk fetch
            data = self.db[list(bytes.int_to_bytes(key) for key in range(self.curr_idx, self.last_exclusive_idx))]

            # cache store
            image_with_label = []
            for item in data:
                buff = io.BytesIO()
                buff.write(item)
                buff.seek(0)
                image_with_label.append(torch.load(buff))

            self.image_with_label = image_with_label
                
        # find the relative index within cache data
        relative_idx = self.curr_idx % len(self.image_with_label)
        
        # advance to next index
        self.curr_idx = self.curr_idx + 1
        return self.image_with_label[relative_idx]

    def cleanup(self):
        self.db.close()