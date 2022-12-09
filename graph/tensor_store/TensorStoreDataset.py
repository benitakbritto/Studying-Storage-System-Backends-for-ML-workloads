'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

from tensor_store.helper import int_to_bytes
from torch.utils.data import Dataset
import tensor_store.constants as constants

class TensorStoreDataset(Dataset):

    def __init__(self, db):
        self.len = constants.INPUT_LEN
        self.db = db

    def __len__(self):
        return self.len
    
    def __getitem__(self, idx):
        key_in_bytes = int_to_bytes(idx)
        val_in_bytes = self.db.read(key_in_bytes).result().value
        return val_in_bytes.decode()
    