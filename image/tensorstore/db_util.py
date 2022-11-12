import tensorstore as ts
from torchvision.datasets import CIFAR100
import torchvision.transforms as tt
import torch
from torch.utils.data import DataLoader
import constants
import PrepareData as prep

def dump_to_db():
    input_data = prep.PrepareData().getInputData()
    dataset = ts.open({
        'driver': 'n5',
        'kvstore': {
            'driver': 'file',
            'path': constants.PATH_TO_KV_STORE,
        },
        'metadata': {
            'compression': {
                'type': 'gzip'
            },
            'dataType': 'float32',
            'dimensions': [len(input_data), constants.IMAGE_SIZE + constants.LABEL_SIZE],
            'blockSize': [100, 100],
        },
        'create': True,
        'delete_existing': True,
    }).result()

    data_train = DataLoader(
            input_data,
            batch_size = constants.BATCH_SIZE,
            shuffle = False, 
            num_workers = 4
        )

    i = 0
    for _, (images, labels) in enumerate(data_train):
        # import pdb; pdb.set_trace()
        size = len(labels)
        labels = labels.reshape(size, 1)
        images = images.reshape(size, 3*32*32)
        imlabels = torch.cat((images, labels), -1)
        write_future = dataset[i:i+size, :].write(imlabels)
        i+=size

    print("Loaded")

if __name__ == "__main__":
    dump_to_db()
