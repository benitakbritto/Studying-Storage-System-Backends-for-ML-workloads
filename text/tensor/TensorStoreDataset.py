'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import tensor.constants as constants
import json
from torch.utils.data import Dataset
from tensor.helper import int_to_bytes

class TensorStoreDataset(Dataset):
    
    def __init__(self, store):
        self.store = store
        self.len = store.len

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        val = self.store.db.read(int_to_bytes(idx)).result().value
        val = json.loads(val.decode())
        return val['text'], val['target']
   