import tiledb
import constants
from torch.utils.data import Dataset

class TileDBDataset(Dataset):
    def __init__(self):
        with tiledb.open(constants.tileUri, 'r') as A:
            self.len = len(A)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        with tiledb.open(constants.tileUri, 'r') as A:
            tldb_row = A[idx]
            return tldb_row['target'], tldb_row['text']


if __name__ == "__main__":
    twitter = TileDBDataset()

    for i in range(0, 10):
        print(twitter.__getitem__(i))
