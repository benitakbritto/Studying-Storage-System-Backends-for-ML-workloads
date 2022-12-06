'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''


from torch.utils.data import Dataset, DataLoader
import tensorstore as ts
import constants
import time

class TensorStoreDataset(Dataset):
    def __init__(self):
        self.dataset = ts.open({
            'driver': 'n5',
            'kvstore': {
                'driver': 'file',
                'path': constants.PATH_TO_KV_STORE ,
            },
            'metadata': {
                'compression': {
                    'type': 'raw'
                },
                'dataType': 'float32',
                'dimensions': [constants.INPUT_SIZE, constants.IMAGE_SIZE + constants.LABEL_SIZE],
                'blockSize': [1024, 3073],
            },
        }).result()

    def __getitem__(self, index):
        # import pdb; pdb.set_trace()
        data = self.dataset[index : index+1, : ].read().result()
        return data
    
    def __len__(self):
        return constants.INPUT_SIZE

if __name__=='__main__':
    ds = TensorStoreDataset()
    
    start = time.time()
    output = DataLoader(ds, batch_size = 1000, num_workers = 0)
    read = 0

    for tensor in output:
        read += tensor.shape[0]

    end = time.time()
    
    print(f'Elapsed time = {end - start}')
    print(f'Items read = {read}')
