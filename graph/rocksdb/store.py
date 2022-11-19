'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''
import rocksdb3
import constants
from csv import reader
import helper as bytes

class RocksDBStore:
    def __init__(self):
        self.db = rocksdb3.open_default(constants.DB_PATH)
        self.len = 0
    
    # Read dataset file and put to rocksdb
    # saves key as rowIndex
    # saves value as the row data in train.txt
    def store_dataset(self):
        row_index = 0
        with open(constants.DATASET_PATH, 'r') as file:
            for line in file:
                key_in_bytes = bytes.int_to_bytes(row_index)
                value_in_bytes = line.encode()

                self.db.put(key_in_bytes, value_in_bytes)

                row_index += 1

        print(f'[DEBUG] At end of function, row_index = {row_index}')
        self.len = row_index

    def write_metadata_to_db(self):
        self.db.put(constants.LEN_KEY.encode(), bytes.int_to_bytes(self.len))

'''
    Driver
'''
if __name__ == "__main__":
    store = RocksDBStore()
    store.store_dataset()
    store.write_metadata_to_db()


