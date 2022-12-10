'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: 
    @authors: Benita, Hemal, Reetuparna
'''

from torch.utils.data import DataLoader, Dataset
import pandas as pd
import time 
import argparse
from tensor_store.PrepareData import PrepareData

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-num-workers",
    help="Number of workers",
    default=0,
    required=False)
parser.add_argument("-batch-size",
    help="Batch size for the dataloader",
    default=256,
    required=False)
parser.add_argument("-input-file",
    help="file for input data",
    required=True)


if __name__=='__main__':
    # Example: python baseline_map.py -batch-size 1024 -num-workers 8 -input-file  /mnt/data/dataset/cifar/
    
    # Read arguments from command line
    args = parser.parse_args()

    start = time.time()
    dataset = PrepareData(args.input_file).getInputData() # map style

    dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    shuffle=False,
                    num_workers=int(args.num_workers))
        
    for _, data in enumerate(dataloader):
        pass
    
    end = time.time()
    print(f'time to load = {end - start}s')

