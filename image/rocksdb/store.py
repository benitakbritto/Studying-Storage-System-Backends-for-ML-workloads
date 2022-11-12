'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''


# TODO: Refactor
from torchvision.datasets import CIFAR100
import torchvision.transforms as tt
import torch
import tensorstore as ts
from torch.utils.data import DataLoader
import rocksdb3
import io

def convert_tensor_to_bytes(tensor_data):
    buff = io.BytesIO()
    torch.save(tensor_data, buff)
    buff.seek(0) 
    return buff.read()

# Source: https://blog.jovian.ai/image-classification-of-cifar100-dataset-using-pytorch-8b7145242df1
stats = ((0.5074,0.4867,0.4411),(0.2011,0.1987,0.2025)) 
train_transform = tt.Compose([
    tt.RandomHorizontalFlip(),
    tt.RandomCrop(32,padding=4,padding_mode="reflect"),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

train_data = CIFAR100(download=True,root="../../../../../../mnt/data/dataset/cifar/",transform=train_transform)
train_classes_items = dict()
db = rocksdb3.open_default('./db_path')

BATCH_SIZE = 256
data_train = DataLoader(train_data,BATCH_SIZE,num_workers=4,pin_memory=True,shuffle=True)

for batch_idx, (images, labels) in enumerate(data_train):
    size = len(labels)
    labels = labels.reshape(size, 1)
    images = images.reshape(size, 3*32*32)
    # images | labels
    value_in_tensor = torch.cat((images, labels), -1)
    value_in_bytes = convert_tensor_to_bytes(value_in_tensor)
    key_in_bytes = bytes(batch_idx)
    db.put(key_in_bytes, value_in_bytes)

# Write metadata
db.put('BATCH_SIZE'.encode(), bytes(256))
db.put('IMAGE_DIM'.encode(), bytes(3*32*32))

