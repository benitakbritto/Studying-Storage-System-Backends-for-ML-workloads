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
            # way 1: get the entire row
            # tldb_row = A[idx]
            
            # way 2: only fetch wanted attributes
            tldb_row = A.query(attrs=("target", "text"), coords=False, order='G')[idx]
            # print(tldb_row)

            return tldb_row['target'], tldb_row['text']


if __name__ == "__main__":
    twitter = TileDBDataset()

    for i in range(0, 3):
        target, text = twitter.__getitem__(i)
        print(target, text)
