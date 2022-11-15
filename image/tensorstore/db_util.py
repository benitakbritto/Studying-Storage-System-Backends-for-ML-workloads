import tensorstore as ts
import torchvision.transforms as tt
import torch
from torch.utils.data import DataLoader
import constants
from PrepareData import PrepareData
import time

def dump_to_db():
    input_data = PrepareData().getInputData()
    dataset = ts.open({
        'driver': 'n5',
        'kvstore': {
            'driver': 'file',
            'path': constants.PATH_TO_KV_STORE,
        },
        'metadata': {
            'compression': {
                'type': 'raw'
            },
            'dataType': 'float32',
            'dimensions': [len(input_data), constants.IMAGE_SIZE + constants.LABEL_SIZE],
            'blockSize': [1000, 100],
        },
        'create': True,
        'delete_existing': True,
    }).result()

    data_train = DataLoader(
            input_data,
            batch_size = constants.BATCH_SIZE,
            shuffle = False, 
            num_workers = 8
        )

    i = 0
    for _, (images, labels) in enumerate(data_train):
        # import pdb; pdb.set_trace()
        size = len(labels)
        labels = labels.reshape(size, constants.LABEL_SIZE)
        images = images.reshape(size, constants.IMAGE_SIZE)
        imlabels = torch.cat((images, labels), -1)
        dataset[i:i+size, :].write(imlabels).result()
        i+=size

    print("Loaded")

if __name__ == "__main__":
    start = time.time()
    dump_to_db()
    end = time.time()
    print(f'elapsed time = {end-start}')
