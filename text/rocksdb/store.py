'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''
import json
import rocksdb3
import constants
from csv import reader
import twitter_dataset as twitter
import helper as bytes

class RocksDBLoader:
    def __init__(self):
        self.db = rocksdb3.open_default(constants.DB_PATH)
        self.len = 0
    
    # Read dataset file and put to rocksdb
    # saves key as rowIndex
    # saves value as byte encoded json obj of the TwitterDataset class
    def load_dataset(self):
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
                
                self.db.put(key, val)

                row_index += 1

        print(f'[DEBUG] At end of function, row_index = {row_index}')
        self.len = row_index

    def write_metadata_to_db(self, key):
        self.db.put(key.encode(), bytes.int_to_bytes(self.len))

    # For debugging
    def read_from_db(self, key):
        key_in_bytes = None
        if isinstance(key, int):
            key_in_bytes = bytes.int_to_bytes(key)
        elif isinstance(key, str):
            key_in_bytes = key.encode()


        val = self.db.get(key_in_bytes)
        assert val is not None

        if key == "TEXT_WORKLOAD":
            val_as_int = bytes.bytes_to_int(val)
            print(f'[DEBUG] val = {val_as_int}')    
        else:
            val_as_json = json.loads(val.decode())
            print(f'[DEBUG] val = {val_as_json}')


    # For debugging
    def delete_db(self):
        del self.db
        rocksdb3.destroy(constants.DB_PATH)            


'''
    Driver
'''
if __name__ == "__main__":
    loader = RocksDBLoader()
    loader.load_dataset()
    loader.write_metadata_to_db(constants.METADATA_KEY)

