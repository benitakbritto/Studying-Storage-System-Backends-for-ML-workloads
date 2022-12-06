import tiledb
from torch.utils.data import Dataset
import numpy as np

class TileDBMapDataset(Dataset):
    def __init__(self, size, tile_uri):
        self.tile_uri = tile_uri
        self.len = size        

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        with tiledb.open(self.tile_uri, 'r') as A:
            data = A.query(attrs=("im", "label"), coords=False, order='G')[idx]

            im = data['im']
            # we stored as tuple, now transform back to array
            im = np.array([list(t) for t in im])
            
            return im, data['label']
