'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import torch
from rocksdict import Rdict
from torch.utils.data import Dataset, DataLoader
import helper as bytes
import constants
import json
import time

class RocksDBDataset(Dataset):
    def __init__(self):
        self.db = Rdict(constants.DB_PATH)

    def __len__(self):
        val = self.db[constants.METADATA_KEY.encode()]
        assert val is not None
        return bytes.bytes_to_int(val)
    
    # returns the text and target attribute from a row
    def __getitem__(self, idx):
        val = self.db[bytes.int_to_bytes(idx)]
        val = json.loads(val.decode())
        return val['text'], val['target']
        
if __name__ == "__main__":
    twitter = RocksDBDataset()
    start = time.time()
    
    # TODO: Tweak these values
    data_train = torch.utils.data.DataLoader(
        twitter,
        batch_size=4,
        shuffle=False, 
        num_workers=0
    )

    i = 0
    for batch_idx, samples in enumerate(data_train):
        i = batch_idx
    
    end = time.time()
    print(f'Elapsed time = {end - start}')
        
