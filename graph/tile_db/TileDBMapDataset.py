import tiledb
from torch.utils.data import Dataset

class TileDBMapDataset(Dataset):
    def __init__(self, size, tile_uri):
        self.tile_uri = tile_uri
        self.len = size        

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        with tiledb.open(self.tile_uri, 'r') as A:
            data = A.query(attrs=("head", "edge", "tail"), coords=False, order='G')[idx]
        return data["head"], data["edge"], data["tail"]
