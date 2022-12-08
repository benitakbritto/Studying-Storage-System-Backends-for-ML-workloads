'''
    @brief: Map style Data loader
    @prereq: bash
    @usage: from main.py
    @authors: Benita, Hemal, Reetuparna
'''

import torch
from rocksdict import Rdict, AccessType
from torch.utils.data import Dataset, DataLoader
import rocksDB.helper as bytes
import rocksDB.constants
import json
import time
import io

class RocksDBMapStyleDataset(Dataset):
    def __init__(self):
        self.db = Rdict(rocksDB.constants.DB_PATH, access_type = AccessType.read_only(False))
        self.num_keys = bytes.bytes_to_int(self.db[rocksDB.constants.NUM_KEYS.encode()])
        # print(f'[DEBUG] num_keys = {self.num_keys}')
        self.rows_in_key = bytes.bytes_to_int(self.db[rocksDB.constants.NUM_ROWS_PER_KEY.encode()])
        # print(f'[DEBUG] rows_in_key = {self.rows_in_key}')
        self.cache = []
        self.count = 0
        self.key_idx_in_mem = -1

    def __len__(self):
        val = self.db[rocksDB.constants.NUM_ROWS.encode()]
        assert val is not None
        return bytes.bytes_to_int(val)
    
    def get_offset(self, idx):
        return idx % self.rows_in_key
    
    def get_key_index(self, idx):
        return idx // self.rows_in_key
    
    def get_data_from_db(self, key_index):
        buff = io.BytesIO()
        val = self.db[bytes.int_to_bytes(key_index)]
        buff.write(val)
        buff.seek(0)
        self.count += 1
        return torch.load(buff)

    # returns the text and target attribute from a row
    def __getitem__(self, idx):
        key_index = self.get_key_index(idx)
        offset = self.get_offset(idx)

        if self.key_idx_in_mem != key_index:
            self.key_idx_in_mem = key_index
            self.cache = self.get_data_from_db(key_index)
        
        val = self.cache[offset]
        val = json.loads(val)
        return val['text'], val['target']