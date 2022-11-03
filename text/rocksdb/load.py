'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''
import json
import rocksdb3
from csv import reader

'''
    Constants
'''
DATASET_PATH = '/mnt/data/dataset/twitter/twitter_clean.csv'
DB_PATH = './db_path'

class TwitterDataset:
    def __init__(self, target, ids, date, flag, user, text):
        self.target = target
        self.ids = ids
        self.date = date
        self.flag = flag
        self.user = user
        self.text = text
   
    # convert data members to json
    def to_json(self):
        return json.dumps(self, indent = 4, default=lambda o: o.__dict__)

class RocksDBLoader:
    def __init__(self):
        self.db = rocksdb3.open_default(DB_PATH)
    
    # helper
    def int_to_bytes(self, x):
        return x.to_bytes((x.bit_length() + 7), 'big')

    # Read dataset file and put to rocksdb
    # saves key as rowIndex
    # saves value as byte encoded json obj of the TwitterDataset class
    def load_dataset(self):
        row_index = 0
        with open(DATASET_PATH, 'r') as read_obj:
            csv_reader = reader(read_obj)
            
            for row_data in enumerate(csv_reader):
                row_data_list = row_data[1]
                dataset_obj = TwitterDataset(row_data_list[0], 
                                            row_data_list[1], 
                                            row_data_list[2], 
                                            row_data_list[3], 
                                            row_data_list[4], 
                                            row_data_list[5])
                
                json_string = dataset_obj.to_json()
                key = self.int_to_bytes(row_index)
                val = json_string.encode()
                
                self.db.put(key, val)

                row_index += 1

        print(f'[DEBUG] At end of function, row_index = {row_index}')


    # For debugging
    def read_from_db(self, key):
        key_in_bytes = self.int_to_bytes(key)
        val = self.db.get(key_in_bytes).decode()
        decode_obj = json.loads(val)
        print(f'[DEBUG] Decoded_obj = {decode_obj}')

    # For debugging
    def delete_db(self):
        del self.db
        rocksdb3.destroy(DB_PATH)            


'''
    Driver
'''
if __name__ == "__main__":
    loader = RocksDBLoader()
    loader.load_dataset()

