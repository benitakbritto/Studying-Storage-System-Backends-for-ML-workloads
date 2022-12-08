'''
    @brief: Storing single value or multiple values per key by reading data 
        from the filesystem and storing it in storage backends
    @prereq: bash
    @usage: python <filename> --rows-per-key <num>
    @authors: Benita, Hemal, Reetuparna
'''
from rocksdict import Rdict
import rocksDB.constants
from csv import reader
import rocksDB.helper as bytes
import time
import io
import torch

class RocksDBStore:
    def __init__(self, input_file, rows_per_key):
        self.db = Rdict(rocksDB.constants.DB_PATH)
        self.num_keys = 0
        self.num_rows = 0
        self.data = []
        self.current_size = 0
        self.target_size = rows_per_key
        self.input_file = input_file

    def convert_tensor_to_bytes(self, tensor_data):
        buff = io.BytesIO()
        torch.save(tensor_data, buff)
        buff.seek(0) 
        return buff.read()

    def store_data(self):
        key_index = 0
        with open(self.input_file, 'r') as file:
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

        # print(f'[DEBUG] At end of function, nums_rows = {self.num_rows}')

    def store_metadata(self):
        self.db[rocksDB.constants.NUM_KEYS.encode()] = bytes.int_to_bytes((int)(self.num_rows / self.target_size) + (self.num_rows % self.target_size != 0))
        self.db[rocksDB.constants.NUM_ROWS_PER_KEY.encode()] = bytes.int_to_bytes(self.target_size)
        self.db[rocksDB.constants.NUM_ROWS_LAST_KEY.encode()] = bytes.int_to_bytes(self.num_rows % self.target_size)
        self.db[rocksDB.constants.NUM_ROWS.encode()] = bytes.int_to_bytes(self.num_rows)

    def cleanup(self):
        self.db.close()
