'''
    @brief: TODO: Add better desc, supports storing single value or multiple values per key
    @prereq: bash
    @usage: python <filename> --rows-per-key <num>
    @authors: Benita, Hemal, Reetuparna
'''
import json
from rocksdict import Rdict
import constants
from csv import reader
import twitter_dataset as twitter
import helper as bytes
import time
import argparse
import io
import torch

parser = argparse.ArgumentParser(description='Store dataset in RocksDB')
parser.add_argument('--rows-per-key', type=int, default=1, help='The number of rows to be store within a key')
args = parser.parse_args()

class RocksDBLoader:
    def __init__(self):
        self.db = Rdict(constants.DB_PATH)
        self.num_keys = 0
        self.num_rows = 0
        self.data = []
        self.current_size = 0
        self.target_size = args.rows_per_key
    
    def convert_tensor_to_bytes(self, tensor_data):
        buff = io.BytesIO()
        torch.save(tensor_data, buff)
        buff.seek(0) 
        return buff.read()

    def store_data(self):
        key_index = 0
        
        with open(constants.DATASET_PATH, 'r', encoding=constants.INPUT_FILE_ENCODING) as read_obj:
            csv_reader = reader(read_obj)
            
            for row_data in enumerate(csv_reader):
                row_data_list = row_data[1]
                dataset_obj = twitter.TwitterDataset(row_data_list[0], 
                    row_data_list[1], 
                    row_data_list[2], 
                    row_data_list[3], 
                    row_data_list[4], 
                    row_data_list[5])
                
                json_string = dataset_obj.to_json()
                self.data.append(json_string)
                self.current_size += 1

                if self.current_size == self.target_size:
                    key = bytes.int_to_bytes(key_index)
                    self.db[key] = self.convert_tensor_to_bytes(self.data)

                    # restore
                    self.data = []
                    self.current_size = 0

                    # next key
                    key_index += 1
                
                self.num_rows += 1
                
        # last batch
        if self.current_size != 0:
            key_in_bytes = bytes.int_to_bytes(key_index)
            self.db[key_in_bytes] = self.convert_tensor_to_bytes(self.data)
        
        print(f'[DEBUG] At end of function, nums_rows = {self.num_rows}')

    # Store the number of rows in this dataset
    def store_metadata(self):
        self.db[constants.NUM_KEYS.encode()] = bytes.int_to_bytes(self.num_rows // self.target_size + (self.num_rows % self.target_size != 0))
        self.db[constants.NUM_ROWS_PER_KEY.encode()] = bytes.int_to_bytes(self.target_size)
        self.db[constants.NUM_ROWS_LAST_KEY.encode()] = bytes.int_to_bytes(self.num_rows % self.target_size)
        self.db[constants.NUM_ROWS.encode()] = bytes.int_to_bytes(self.num_rows)

    def cleanup(self):
        self.db.close()

'''
    Driver
'''
if __name__ == "__main__":
    store = RocksDBLoader()

    start = time.time()
    store.store_data()
    store.store_metadata()

    end = time.time()

    print(f'Elapsed time = {end - start}')

    store.cleanup()

