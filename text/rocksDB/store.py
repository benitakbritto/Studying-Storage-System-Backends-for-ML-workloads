'''
    @brief: Storing single value or multiple values per key by reading data 
        from the filesystem and storing it in storage backends
    @prereq: bash
    @usage: from main.py
    @authors: Benita, Hemal, Reetuparna
'''

from rocksdict import Rdict
import rocksDB.constants
from csv import reader
import rocksDB.twitter_dataset as twitter
import rocksDB.helper as bytes
import io
import torch

class RocksDBStore:
    def __init__(self, input_file, rows_per_key):
        self.db = Rdict(rocksDB.constants.DB_PATH)
        self.num_keys = 0
        self.num_rows = 0
        self.data = []
        self.current_size = 0
        self.target_size = int(rows_per_key)
        self.input_file = input_file
    
    def convert_tensor_to_bytes(self, tensor_data):
        buff = io.BytesIO()
        torch.save(tensor_data, buff)
        buff.seek(0) 
        return buff.read()

    def store_data(self):
        key_index = 0
        
        with open(self.input_file, 'r', encoding=rocksDB.constants.INPUT_FILE_ENCODING) as read_obj:
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
        
        # print(f'[DEBUG] At end of function, nums_rows = {self.num_rows}')

    # Store the number of rows in this dataset
    def store_metadata(self):
        self.db[rocksDB.constants.NUM_KEYS.encode()] = bytes.int_to_bytes(self.num_rows // self.target_size + (self.num_rows % self.target_size != 0))
        self.db[rocksDB.constants.NUM_ROWS_PER_KEY.encode()] = bytes.int_to_bytes(self.target_size)
        self.db[rocksDB.constants.NUM_ROWS_LAST_KEY.encode()] = bytes.int_to_bytes(self.num_rows % self.target_size)
        self.db[rocksDB.constants.NUM_ROWS.encode()] = bytes.int_to_bytes(self.num_rows)
    
    def cleanup(self):
        self.db.close()