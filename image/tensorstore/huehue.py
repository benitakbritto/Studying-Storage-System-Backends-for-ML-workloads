import tensorstore as ts
import numpy as np
from torch.utils.data import DataLoader, Dataset
import time

class TensorStoreImageDataset(Dataset):

    def __init__(self):
        self.dataset = ts.open({
            'driver': 'n5',
            'kvstore': {
                'driver': 'file',
                'path': '/mnt/data/store/',
            },
            'metadata': {
                'compression': {
                    'type': 'gzip'
                },
                'dataType': 'float32',
                'dimensions': [50000, 3073],
                'blockSize': [100, 100],
            },
        }).result()


    def __len__(self):
        return self.dataset.shape[0]

    def __getitem__(self, idx):
        val = self.dataset[idx, :].read().result()


batch_size = 256
# Load data
start = time.time()    

image_dataset = TensorStoreImageDataset()
# import pdb; pdb.set_trace()

# TODO: Tweak these values
data_train = DataLoader(
    image_dataset,
    batch_size=batch_size,
    shuffle=False, 
    num_workers=4
)


i = 0
for batch_idx, samples in enumerate(data_train):
    i = batch_idx

end = time.time()
print(f'Elapsed time in loading = {end - start}')