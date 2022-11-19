'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''
import json
from rocksdict import Rdict
import constants
from csv import reader
import twitter_dataset as twitter
import helper as bytes
import time

class RocksDBLoader:
    def __init__(self):
        self.db = Rdict(constants.DB_PATH)
        self.len = 0
    
    # Read dataset file and put to rocksdb
    # saves key as rowIndex
    # saves value as byte encoded json obj of the TwitterDataset class
    def store_data(self):
        row_index = 0
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
                key = bytes.int_to_bytes(row_index)
                val = json_string.encode()
                
                self.db[key] = val

                row_index += 1

        print(f'[DEBUG] At end of function, row_index = {row_index}')
        self.len = row_index

    # Store the number of rows in this dataset
    def store_metadata(self):
        self.db[constants.METADATA_KEY.encode()] = bytes.int_to_bytes(self.len)

'''
    Driver
'''
if __name__ == "__main__":
    start = time.time()
    loader = RocksDBLoader()
    loader.store_data()
    loader.store_metadata()
    end = time.end()

    print(f'Elapsed time = {end - start}')

