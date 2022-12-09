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
    help="Path for input data",
    required=True)

class BaselineTextDataset(Dataset):
    def __init__(self, input_file):
        self.df = pd.read_csv(input_file, encoding='ISO-8859-1').values.tolist()

    def __getitem__(self, index):
        return self.df[index]
    
    def __len__(self):
        return self.df.__len__()


if __name__=='__main__':
    # Example:  python baseline_iterable.py -batch-size 1024 num-workers 8 -input-path /mnt/data/dataset/twitter/twitter_sentiment_dataset.csv
    
    # Read arguments from command line
    args = parser.parse_args()

    start = time.time()
    dataset = BaselineTextDataset(args.input_file)

    dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    shuffle=False,
                    num_workers=int(args.num_workers))
        
    for _, data in enumerate(dataloader):
        pass
    
    end = time.time()
    print(f'time to load = {end - start}s')

