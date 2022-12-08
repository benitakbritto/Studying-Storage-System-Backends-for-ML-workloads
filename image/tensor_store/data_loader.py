'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import tensorstore as ts
import tensor_store.constants as constants
from torch.utils.data import Dataset, DataLoader

class TensorStoreDataset(Dataset):

    def __getitem__(self, index):
        self.db = ts.open({
            'driver': 'n5',
            'kvstore': {
                'driver': 'file',
                'path': constants.PATH_TO_KV_STORE ,
            }
        }).result()
        data = self.db[index : index+1, : ].read().result()
        return data
    
    def __len__(self):
        return constants.INPUT_SIZE

if __name__=='__main__':
    ds = TensorStoreDataset()
    
    output = DataLoader(ds, batch_size = 1000, num_workers = 0)
    read = 0

    for tensor in output:
        read += tensor.shape[0]

    print(f'Items read = {read}')
