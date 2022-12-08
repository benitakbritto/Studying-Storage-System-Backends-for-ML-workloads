'''
    @brief: Map style Data loader
    @prereq: bash
    @usage: from main.py
    @authors: Benita, Hemal, Reetuparna
'''

import torch
from rocksdict import Rdict, AccessType
from torch.utils.data import Dataset, DataLoader, get_worker_info
import time
import io
import rocksDB.constants
import rocksDB.helper as bytes

class RocksDBMapStyleDataset(Dataset):
    def __init__(self):
        self.db = Rdict(rocksDB.constants.DB_PATH, 
            access_type = AccessType.read_only(False))
        self.num_rows_in_key = bytes.bytes_to_int(self.db[rocksDB.constants.NUM_OF_ROWS_IN_KEY.encode()])
        assert self.num_rows_in_key is not None 
        self.image_dim = bytes.bytes_to_int(self.db[rocksDB.constants.IMAGE_DIM.encode()]) + 1
        assert self.image_dim is not None 
        self.key_idx_in_mem = -1
        self.cache = torch.empty(self.num_rows_in_key, self.image_dim)
        self.count = 0

    def __len__(self):
        val = self.db[rocksDB.constants.NUM_OF_IMAGES.encode()]
        assert val is not None
        return bytes.bytes_to_int(val)
    
    def get_offset(self, idx):
        return idx % self.num_rows_in_key
    
    def get_key_index(self, idx):
        return idx // self.num_rows_in_key
    
    def get_data_from_db(self, key_index):
        buff = io.BytesIO()
        val = self.db[bytes.int_to_bytes(key_index)]
        buff.write(val)
        buff.seek(0)
        self.count += 1
        return torch.load(buff)

    # return image tensor, label
    def __getitem__(self, idx):
        key_index = self.get_key_index(idx)
        offset = self.get_offset(idx)

        if self.key_idx_in_mem != key_index:
            self.key_idx_in_mem = key_index
            self.cache = self.get_data_from_db(key_index)
        
        return self.cache[offset]
        
