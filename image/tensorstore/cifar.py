
from torchvision.datasets import CIFAR100
import torchvision.transforms as tt
import torch
import tensorstore as ts
from torch.utils.data import Dataset, DataLoader
import numpy as np

stats = ((0.5074,0.4867,0.4411),(0.2011,0.1987,0.2025))
train_transform = tt.Compose([
    tt.RandomHorizontalFlip(),
    tt.RandomCrop(32,padding=4,padding_mode="reflect"),
    tt.ToTensor(),
    tt.Normalize(*stats)
])

train_data = CIFAR100(download=True,root="../../../../../../mnt/data/dataset/cifar/",transform=train_transform)

train_classes_items = dict()

dataset = ts.open({
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
        'dimensions': [len(train_data), 3*32*32 + 1],
        'blockSize': [100, 100],
    },
    'create': True,
    'delete_existing': True,
}).result()


batch_size = 256

data_train = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=False, 
        num_workers=4
    )

i = 0
for batch_idx, (images, labels) in enumerate(data_train):
    # import pdb; pdb.set_trace()
    size = len(labels)
    labels = labels.reshape(size, 1)
    images = images.reshape(size, 3*32*32)
    imlabels = torch.cat((images, labels), -1)
    write_future = dataset[i:i+size, :].write(imlabels)
    i+=size

import pdb; pdb.set_trace()