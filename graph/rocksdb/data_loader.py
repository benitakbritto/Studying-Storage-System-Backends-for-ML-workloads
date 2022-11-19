'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import torch
import rocksdb3
from torch.utils.data import Dataset
import helper as bytes
import constants
import json
import time

class RocksDBDataset(Dataset):
    def __init__(self):
        self.db = rocksdb3.open_default(constants.DB_PATH)

    def __len__(self):
        val = self.db.get(constants.LEN_KEY.encode())
        assert val is not None
        return bytes.bytes_to_int(val)
    
    # returns the head, relation, tail as a list of strings
    def __getitem__(self, idx):
        val = self.db.get(bytes.int_to_bytes(idx)).decode()
        return val.split()
        
if __name__ == "__main__":
    fb15k = RocksDBDataset()
    start = time.time()
    
    # TODO: Tweak these values
    data_train = torch.utils.data.DataLoader(
        fb15k,
        batch_size=4,
        shuffle=False, 
        num_workers=0
    )

    i = 0
    for batch_idx, samples in enumerate(data_train):
        i = batch_idx
    
    end = time.time()
    print(f'Elapsed time = {end - start}')
        
