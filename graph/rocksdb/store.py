'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename> --rows-per-key <num>
    @authors: Benita, Hemal, Reetuparna
'''
from rocksdict import Rdict
import constants
from csv import reader
import helper as bytes
import time
import argparse
import io
import torch

parser = argparse.ArgumentParser(description='Store dataset in RocksDB')
parser.add_argument('--rows-per-key', type=int, default=1, help='The number of rows to be store within a key')
args = parser.parse_args()

class RocksDBStore:
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
        with open(constants.DATASET_PATH, 'r') as file:
            for line in file:
                self.data.append(line)
                self.current_size += 1

                if self.current_size == self.target_size:
                    key_in_bytes = bytes.int_to_bytes(key_index)
                    self.db[key_in_bytes] = self.convert_tensor_to_bytes(self.data)

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

    def store_metadata(self):
        self.db[constants.NUM_KEYS.encode()] = bytes.int_to_bytes((int)(self.num_rows / self.target_size) + (self.num_rows % self.target_size != 0))
        self.db[constants.NUM_ROWS_PER_KEY.encode()] = bytes.int_to_bytes(self.target_size)
        self.db[constants.NUM_ROWS_LAST_KEY.encode()] = bytes.int_to_bytes(self.num_rows % self.target_size)
        self.db[constants.NUM_ROWS.encode()] = bytes.int_to_bytes(self.num_rows)

    def cleanup(self):
        self.db.close()

'''
    Driver
'''
if __name__ == "__main__":
    store = RocksDBStore()

    start = time.time()

    store.store_data()
    store.store_metadata()

    end = time.time()

    print(f'Elapsed time = {end - start}')

    store.cleanup()


