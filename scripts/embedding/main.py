import numpy as np
from EmbedddingIterableDataset import EmbedddingIterableDataset
from torch.utils.data import DataLoader

def gen_embedding(size):
    return np.random.random(size=size)

path = "/mnt/data/embeddings/text.txt"
batch_size = 8

dataset = EmbedddingIterableDataset(path=path)
dataloader = DataLoader(dataset, batch_size = batch_size)

for data in dataloader:
    print(data)