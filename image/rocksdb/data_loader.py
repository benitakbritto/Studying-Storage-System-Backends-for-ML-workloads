'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import torch
import rocksdb3
from torch.utils.data import Dataset, DataLoader, get_worker_info
import time
import io
import constants

class RocksDBDataset(Dataset):
    def __init__(self):
        self.db = rocksdb3.open_default('./db_path')
        self.batch_in_key = self.bytes_to_int(self.db.get('BATCH_SIZE'.encode()))
        assert self.batch_in_key is not None 
        self.image_dim = self.bytes_to_int(self.db.get('IMAGE_DIM'.encode())) + 1
        assert self.image_dim is not None 
        self.batch_idx_in_mem = -1
        self.cache = torch.empty(self.batch_in_key, self.image_dim)
        self.count = 0

    def __len__(self):
        val = self.db.get('NUM_OF_IMAGES'.encode())
        assert val is not None
        return self.bytes_to_int(val)
    
    def bytes_to_int(self, xbytes):
        return int.from_bytes(xbytes, 'big')
    
    def int_to_bytes(self, x):
        return x.to_bytes((x.bit_length() + 7), 'big')

    def get_offset(self, idx):
        return idx % self.batch_in_key
    
    def get_batch_index(self, idx):
        return (int) (idx / self.batch_in_key)
    
    def get_data_from_db(self, batch_index):
        buff = io.BytesIO()
        val = self.db.get(self.int_to_bytes(batch_index))
        buff.write(val)
        buff.seek(0)
        self.count += 1
        return torch.load(buff)

    # return image tensor, label
    def __getitem__(self, idx):
        batch_index = self.get_batch_index(idx)
        offset = self.get_offset(idx)

        if self.batch_idx_in_mem != batch_index:
            self.batch_idx_in_mem = batch_index
            self.cache = self.get_data_from_db(batch_index)
        
        return self.cache[offset]
            
if __name__ == "__main__":
    NUM_WORKERS = 0
    cifar = RocksDBDataset()
    start = time.time()
    
    # TODO: Tweak these values
    # Note: Must choose shuffle=False, else out of bounds
    data_train = DataLoader(
        cifar,
        batch_size=constants.BATCH_SIZE,
        shuffle=False, 
        num_workers=NUM_WORKERS
    )

    i = 0
    for batch_idx, samples in enumerate(data_train):
        i = batch_idx
    
    end = time.time()
    print(f'Elapsed time = {end - start}')

    print(f'# calls to db = {cifar.count}')
        
