# TODO: Last batch is failing
'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import torch
from rocksdict import Rdict
from torch.utils.data import Dataset
import helper as bytes
import constants
import json
import time
import io

class RocksDBDataset(Dataset):
    def __init__(self):
        self.db = Rdict(constants.DB_PATH)
        self.num_keys = bytes.bytes_to_int(self.db[constants.NUM_KEYS.encode()])
        print(f'[DEBUG] num_keys = {self.num_keys}')
        self.rows_in_key = bytes.bytes_to_int(self.db[constants.NUM_ROWS_PER_KEY.encode()])
        print(f'[DEBUG] rows_in_key = {self.rows_in_key}')
        self.cache = []
        self.count = 0
        self.key_idx_in_mem = -1

    def __len__(self):
        val = self.db[constants.NUM_ROWS.encode()]
        assert val is not None
        print(f'len = {bytes.bytes_to_int(val)}')
        return bytes.bytes_to_int(val)
    
    def get_offset(self, idx):
        return idx % self.rows_in_key
    
    def get_key_index(self, idx):
        return (int) (idx / self.rows_in_key)
    
    def get_data_from_db(self, key_index):
        buff = io.BytesIO()
        val = self.db[bytes.int_to_bytes(key_index)]
        buff.write(val)
        buff.seek(0)
        self.count += 1
        return torch.load(buff)
    
    # returns the head, relation, tail as a list of strings
    def __getitem__(self, idx):
        key_index = self.get_key_index(idx)
        offset = self.get_offset(idx)

        if self.key_idx_in_mem != key_index:
            self.key_idx_in_mem = key_index
            self.cache = self.get_data_from_db(key_index)
            
        val = (self.cache[offset]).decode()
        return val.split()
        
if __name__ == "__main__":
    fb15k = RocksDBDataset()
    start = time.time()
    
    # TODO: Tweak these values
    data_train = torch.utils.data.DataLoader(
        fb15k,
        batch_size=fb15k.rows_in_key,
        shuffle=False, 
        num_workers=0
    )

    i = 0
    for batch_idx, samples in enumerate(data_train):
        i = batch_idx
    
    end = time.time()
    print(f'Elapsed time = {end - start}')