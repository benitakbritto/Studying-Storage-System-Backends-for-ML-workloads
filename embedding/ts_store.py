from BaseStore import BaseStore
import tensorstore as ts

DB_PATH = '/mnt/data/ts_embedding/'

class TSEmbedding(BaseStore):

    def __init__(self, rows_count, cols_count) -> None:
        self.db = ts.open({
            'driver': 'n5',
            'kvstore': {
                'driver': 'file',
                'path': DB_PATH,
            },
            'metadata': {
                'compression': {
                    'type': 'raw'
                },
                'dataType': 'float32',
                'dimensions': [rows_count, cols_count],
                'blockSize': [1024, 3073],
            },
            'create': True,
            'delete_existing': True,
        }).result()

    def store_data(self, key_list, value_list):
        start_key = key_list[0]
        self.db[start_key : start_key+len(key_list), :].write(value_list).result()

    def get_data(self, key_list):
        start_key = key_list[0]
        data = self.db[start_key : start_key+len(key_list), : ].read().result()
        return data

if __name__ == "__main__":
    tsstore = TSEmbedding(4, 4)

    key_list = [0, 1, 2, 3]
    value_list = [[1, 2, 3, 4], [3, 4, 5, 6], [2, 13,1,2], [1, 3, 3, 4]]

    tsstore.store_data(key_list, value_list)
    ret_list = tsstore.get_data(key_list)

    for index, ret in enumerate(ret_list):
        print(f'ret_{index} = {ret}')
    
    print(tsstore.get_data([3]))