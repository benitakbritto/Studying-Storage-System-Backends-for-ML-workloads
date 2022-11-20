'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename> --rows-per-key <num>
    @authors: Benita, Hemal, Reetuparna

    @resource: https://blog.jovian.ai/image-classification-of-cifar100-dataset-using-pytorch-8b7145242df1
'''

from operator import contains
from torchvision.datasets import CIFAR100
import torchvision.transforms as tt
import torch
import tensorstore as ts
from torch.utils.data import DataLoader
from rocksdict import Rdict
import io
import constants
import time
import argparse

parser = argparse.ArgumentParser(description='Store dataset in RocksDB')
parser.add_argument('--rows-per-key', type=int, default=1, help='The number of rows to be store within a key')
args = parser.parse_args()

class RocksDBStore:
    def __init__(self):
        self.db = Rdict(constants.DB_PATH)
        self.train_data_len = 0

    def convert_tensor_to_bytes(self, tensor_data):
        buff = io.BytesIO()
        torch.save(tensor_data, buff)
        buff.seek(0) 
        return buff.read()

    def int_to_bytes(self, x):
        return x.to_bytes((x.bit_length() + 7), 'big')
    
    def bytes_to_int(self, xbytes):
        return int.from_bytes(xbytes, 'big')

    def store_data(self):
        # Set data transformation
        stats = ((0.5074,0.4867,0.4411),(0.2011,0.1987,0.2025)) 
        train_transform = tt.Compose([
            tt.RandomHorizontalFlip(),
            tt.RandomCrop(32,padding=4,padding_mode="reflect"),
            tt.ToTensor(),
            tt.Normalize(*stats)
        ])

        # Read data
        train_data = CIFAR100(download=True,
                        root=constants.DATASET_PATH,
                        transform=train_transform)
        self.train_data_len = len(train_data)

        # TODO: Tweak these values
        data_train = DataLoader(train_data,
                        args.rows_per_key,
                        num_workers=4,
                        pin_memory=True,
                        shuffle=True)

        # Save data
        for batch_idx, (images, labels) in enumerate(data_train):
            size = len(labels)
            labels = labels.reshape(size, 1)
            images = images.reshape(size, 3*32*32)
            # images | labels
            value_in_tensor = torch.cat((images, labels), -1)
            value_in_bytes = self.convert_tensor_to_bytes(value_in_tensor)
            key_in_bytes = self.int_to_bytes(batch_idx)
            self.db[key_in_bytes] = value_in_bytes

    def store_metadata(self):
        self.db[constants.NUM_OF_ROWS_IN_KEY.encode()] = self.int_to_bytes(args.rows_per_key)
        self.db[constants.IMAGE_DIM.encode()] = self.int_to_bytes(3*32*32)
        self.db[constants.NUM_OF_IMAGES.encode()] = self.int_to_bytes(self.train_data_len)
        self.db[constants.ROWS_LAST_KEY.encode()] = self.int_to_bytes(self.train_data_len % args.rows_per_key)
        self.db[constants.NUM_KEYS.encode()] = self.int_to_bytes((int)(self.train_data_len / args.rows_per_key) + (self.train_data_len % args.rows_per_key != 0))

if __name__ == "__main__":
    store_obj = RocksDBStore()

    start = time.time()
    
    store_obj.store_data()
    store_obj.store_metadata()
    
    end = time.time()
    print(f'Elapsed time = {end - start}')
