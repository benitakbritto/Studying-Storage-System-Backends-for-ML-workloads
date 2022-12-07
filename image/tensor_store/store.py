'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import tensorstore as ts
import torchvision.transforms as tt
import torch
from torch.utils.data import DataLoader
import tensor_store.constants as constants
from tensor_store.PrepareData import PrepareData


class TSStore():
    
    def __init__(self, input_path):
        self.input_data = PrepareData(input_path).getInputData()
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

        self.size = 0

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
        
        self.size = i

        print("Loaded")
