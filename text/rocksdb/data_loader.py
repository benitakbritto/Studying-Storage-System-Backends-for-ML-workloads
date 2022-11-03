'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import torch
import rocksdb3
from torch.utils.data import Dataset, DataLoader
import helper as bytes
import constants
import json

class RocksDBDataset(Dataset):
    def __init__(self):
        self.db = rocksdb3.open_default(constants.DB_PATH)

    def __len__(self):
        val = self.db.get(constants.METADATA_KEY.encode())
        assert val is not None
        return self.bytes_to_int(val)
    
    # returns the text and target attribute from a row
    def __getitem__(self, idx):
        val = self.db.get(bytes.int_to_bytes(idx))
        val = json.loads(val.decode())
        
        return val['text'], val['target']
        
if __name__ == "__main__":
    twitter = RocksDBDataset()

    for i in range(0, 3):
        print(twitter.__getitem__(i))
        
