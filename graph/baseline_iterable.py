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

class BaselineGraphIterableDataset(IterableDataset):
    def __init__(self, input_file):
        triples = list()
        with open(input_file, 'r') as f:
            for line in f:
                head, relation, tail = line.strip().split('\t')
                triples.append((head, relation, tail))
        self.dataset = triples

    def __iter__(self):
        for data in self.dataset:
            yield data


if __name__=='__main__':
    # Example: python baseline_iterable.py -batch-size 1024 -input-path /mnt/data/dataset/fb15k-237/train.txt 

    # Read arguments from command line
    args = parser.parse_args()

    start = time.time()

    dataset = BaselineGraphIterableDataset(args.input_path)

    dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    shuffle=False,
                    num_workers=0)
 
    for _, batch in enumerate(dataloader):
        # import pdb; pdb.set_trace()
        pass
    
    end = time.time()
    print(f'time to load = {end - start}s')

