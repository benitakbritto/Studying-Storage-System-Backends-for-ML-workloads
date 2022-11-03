from time import sleep
import tiledb
import constants
from torch.utils.data import Dataset

class TileDBDataset(Dataset):
    def __init__(self, cache_len):
        # cache store
        self.target = []
        self.text = []

        self.max_exclusive_idx = -1

        # items count to fetch in one shot
        self.cache_len = cache_len

        with tiledb.open(constants.tileUri, 'r') as A:
            self.len = len(A)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        # pre-fetch
        if idx >= self.max_exclusive_idx:
            with tiledb.open(constants.tileUri, 'r') as A:
                # find last index to fetch(exclusive)
                self.max_exclusive_idx = min(idx + self.cache_len, self.len)

                # bulk fetch
                data = A.query(attrs=("target", "text"), coords=False, order='G')[idx: self.max_exclusive_idx]
                
                # cache store
                self.target = data['target']
                self.text = data['text']
                
        # find the relative index within cache data
        relative_idx = idx % len(self.target)
        return self.target[relative_idx], self.text[relative_idx]

if __name__ == "__main__":
    twitter = TileDBDataset(cache_len=10000)
    i = 0

    while i < twitter.len:
        target, text = twitter.__getitem__(i)
        # print(target, text)
        if i%10000 == 0:
            print(i)
        i = i + 1
