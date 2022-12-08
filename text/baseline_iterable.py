'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: 
    @authors: Benita, Hemal, Reetuparna
'''

from torch.utils.data import DataLoader, IterableDataset
import pandas as pd
import time 
import argparse

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-batch-size",
    help="Batch size for the dataloader",
    default=256,
    required=False)
parser.add_argument("-input-path",
    help="Path for input data",
    required=True)

class BaselineTextIterableDataset(IterableDataset):

    def __init__(self, input_path):
        #Store the filename in object's memory
        self.input_path = input_path
        #And that's it, we no longer need to store the contents in the memory

    def __iter__(self):
        #Create an iterator
        file_itr = open(self.input_path, encoding='ISO-8859-1')
        return file_itr


if __name__=='__main__':
    # Example:  python baseline_iterable.py -batch-size 1024 -input-path /mnt/data/dataset/twitter/twitter_sentiment_dataset.csv
    
    # Read arguments from command line
    args = parser.parse_args()

    start = time.time()
    dataset = BaselineTextIterableDataset(args.input_path)

    dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    shuffle=False,
                    num_workers=0) #since we are reading the file sequentially, we cant parallelize the data sampling 
    read = ''
    for i,data in enumerate(dataloader):
        read = data

    end = time.time()
    print(f'time to load = {end - start}s')

