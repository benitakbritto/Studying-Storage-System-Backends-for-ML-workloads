'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

from tensor_store.helper import int_to_bytes
from torch.utils.data import Dataset

class TensorStoreDataset(Dataset):

    def __init__(self, db):
        self.num_rows = 0
        self.db = db
        # print("Store init done")

    def __len__(self):
        return self.num_rows
    
    def __getitem__(self, idx):
        key_in_bytes = int_to_bytes(idx)
        val_in_bytes = self.db.read(key_in_bytes).result().value
        return val_in_bytes.decode()
    