import tiledb
from torch.utils.data import Dataset

class TileDBMapDataset(Dataset):
    def __init__(self, size, tile_uri):
        self.tile_uri = tile_uri
        self.len = size        

    def __len__(self):
        return self.len

    def __getitem__(self, idx): 
        # print(idx)       
        with tiledb.open(self.tile_uri, 'r') as A:
            data = A.query(attrs=("target", "text"), coords=False, order='G')[idx:idx+1]
            return data["target"][0], data["text"][0]
