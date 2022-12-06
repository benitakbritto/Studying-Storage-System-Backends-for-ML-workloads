'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import constants
from torch.utils.data import Dataset

class TensorStoreDataset(Dataset):

    def __init__(self, db):
        self.num_rows = 0
        self.db = db
        # print("Store init done")

    def convert_tensor_to_bytes(self, tensor_data):
        return tensor_data.encode()
    
    def int_to_bytes(self, num):
        str_val = str(num)
        return str_val.encode()

    async def ingestData(self):
        row_index = 0

        with open(constants.DATASET_PATH, 'r') as file:
            for line in file:

                key_in_bytes = self.int_to_bytes(row_index)
                val_in_bytes = self.convert_tensor_to_bytes(line)
                await self.db.write(key_in_bytes, val_in_bytes)
                row_index += 1
                
            self.num_rows = row_index

    def __len__(self):
        return self.num_rows
    
    def __getitem__(self, idx):
        key_in_bytes = self.int_to_bytes(idx)
        val_in_bytes = self.db.read(key_in_bytes).result().value
        return val_in_bytes.decode()
    