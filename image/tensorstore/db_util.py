import tensorstore as ts
import torchvision.transforms as tt
import torch
from torch.utils.data import DataLoader
import constants
from PrepareData import PrepareData
import time

class Store():
    def __init__(self):
        self.input_data = PrepareData().getInputData()
        self.dataset = ts.open({
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
                'dimensions': [len(self.input_data), constants.IMAGE_SIZE + constants.LABEL_SIZE],
                'blockSize': [1024, 3073],
            },
            'create': True,
            'delete_existing': True,
        }).result()

    def dump_to_db(self):
        data_train = DataLoader(
            self.input_data,
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
            self.dataset[i:i+size, :].write(imlabels).result()
            i+=size

        print("Loaded")

if __name__ == "__main__":
    start = time.time()
    store = Store()
    store.dump_to_db()
    end = time.time()
    print(f'elapsed time = {end-start}')
