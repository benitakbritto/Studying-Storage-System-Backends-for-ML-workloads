from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import tiledb
import torch
import torchvision
# TODO: change this import relative to the main 
import constants as constants
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import numpy as np

def create_tiledb_schema(rows_count, cols_count):

    # Create the dimension, inclusive of both end
    d1 = tiledb.Dim(domain=(0, rows_count - 1), tile=2, dtype=np.int32)
    d2 = tiledb.Dim(domain=(0, cols_count - 1), tile=2, dtype=np.int32)

    # Create a domain using the two dimensions
    dom = tiledb.Domain(d1, d2)

    # Create a dummy attr, required
    attr = tiledb.Attr(name="im_label", dtype=np.float32)

    # Create the array schema, setting `sparse=False` to indicate a dense array
    schema = tiledb.ArraySchema(domain=dom, attrs=[attr])

    tiledb.DenseArray.create(constants.tileUri, schema, overwrite=True)

    # print('TileDB schema created')

def write_to_tldb(row_start, row_end, col_start, col_end, data):
    with tiledb.DenseArray(constants.tileUri, mode='w') as A:
        A[row_start:row_end, col_start:col_end] = data
    
    # print(f'from:{row_start} to {row_end} is written')
    

def dump_to_db():
    # pytorch params
    batch_size = 50000/8
    max_workers = 8

    transform = transforms.Compose([transforms.ToTensor()])
    trainset = torchvision.datasets.CIFAR100(root=constants.rootDir, train=True,
                                            download=True, transform=transform)

    image_len = 3*32*32 + 1
    create_tiledb_schema(rows_count=len(trainset), cols_count = image_len)

    trainloader = DataLoader(trainset, batch_size=batch_size,
                                            shuffle=False, num_workers=max_workers)

    # Setting start method to 'spawn' is required to
    # avoid problems with process global state when spawning via fork.
    # NOTE: *must be inside __main__* or a function.
    if multiprocessing.get_start_method(True) != "spawn":
        multiprocessing.set_start_method("spawn", True)

    i = 0
    tasks = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for batch_idx, (images, labels) in enumerate(trainloader):
            size = len(labels)
            labels = labels.reshape(size, 1)
            images = images.reshape(size, 3*32*32)

            im_with_labels = torch.cat((images, labels), -1)

            # print(f'batch_idx:{batch_idx} is converted')
            data = im_with_labels.numpy(force=False)
            
            task = executor.submit(write_to_tldb, *(i, i + size, 0, image_len, data))

            tasks.append(task)

            # next
            i += size

    # print("Task results: ", [t.result() for t in tasks])

if __name__ == "__main__":
    dump_to_db()
    
    pass