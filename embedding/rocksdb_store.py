'''
    @brief: TODO
    @prereq: bash
    @usage: TODO
    @authors: Benita, Hemal, Reetuparna
'''

from BaseStore import BaseStore
from rocksdict import Rdict, WriteBatch

DB_PATH = './rocks_embedding_path'

class RocksDBEmbedding(BaseStore):
    def __init__(self):
        self.db = Rdict(DB_PATH)

    def int_to_bytes(self, x):
        return x.to_bytes((x.bit_length() + 7), 'big')
    
    def bytes_to_int(self, xbytes):
        return int.from_bytes(xbytes, 'big')
    
    # stores a list of embeddings
    def store_data(self, key_list, value_list):
        wb = WriteBatch()
        
        for index, key in enumerate(key_list):
            key_in_bytes = self.int_to_bytes(key)
            value_in_bytes = bytearray(value_list[index])
            wb.put(key_in_bytes, value_in_bytes)
        
        self.db.write(wb)

    # returns a list of embeddings
    # returns empty list if key does not exist
    def get_data(self, key_list):
        value_list = []
        key_list_in_bytes = []

        for key in key_list:
            key_list_in_bytes.append(self.int_to_bytes(key))

        ret_list = self.db[key_list_in_bytes]
        for ret in ret_list:
            value_list.append(list(ret) if ret is not None else [])

        return value_list

# if __name__ == "__main__":
#     rocksdb = RocksDBEmbedding()

#     key_list = [1, 2, 3, 4]
#     value_list = [[1, 2, 3, 4], [3, 4, 5, 6], [2, 13], [1, 3, 4]]

#     rocksdb.store_data(key_list, value_list)
#     ret_list = rocksdb.get_data(key_list)

#     for index, ret in enumerate(ret_list):
#         print(f'ret_{index} = {ret}')
    
#     print(rocksdb.get_data([5]))