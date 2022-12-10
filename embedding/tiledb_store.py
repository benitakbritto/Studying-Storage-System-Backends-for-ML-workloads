import tiledb
import numpy as np
from BaseStore import BaseStore

class TileDBEmbedding(BaseStore):

    def __init__(self, tile_uri, rows_count, cols_count):
        self.tile_uri = tile_uri
        self.rows_count = rows_count
        self.cols_count = cols_count

        self.np_tuple_type =  ','.join('f4' for _ in range(0, cols_count))
        self.__create_tiledb_schema__(rows_count=rows_count, tile_uri=tile_uri)

    def __create_tiledb_schema__(self, rows_count, tile_uri):
        # Create the dimension, inclusive of both end
        d1 = tiledb.Dim(domain=(0, rows_count - 1), tile=2, dtype=np.int32)

        # Create a domain using the dimension
        dom = tiledb.Domain(d1)

        # Create a dummy attr, required
        # np_tuple_type = ','.join('f4' for _ in range(0, cols_count))
        em_attr = tiledb.Attr(name="em", dtype=np.dtype(self.np_tuple_type))

        # Create the array schema, setting `sparse=False` to indicate a dense array
        schema = tiledb.ArraySchema(domain=dom, attrs=[em_attr], sparse=True)

        tiledb.SparseArray.create(tile_uri, schema, overwrite=True)

        # print('TileDB schema created')
    
    def get_unique_kv(self, key_list, value_list):
        kv = dict()

        for i, key in enumerate(key_list):
            kv[key] = value_list[i]
        
        keys = []
        values = []

        for k, v in kv.items():
            keys.append(k)
            values.append(v)
        
        return keys, values

    def store_data(self, key_list, value_list):
        # sparse array does not support duplicate keys, so building unique kv pairs
        keys, values = self.get_unique_kv(key_list=key_list, value_list=value_list)

        # convert to tuple of embedding_len
        data = np.array([tuple(row) for row in values], dtype=self.np_tuple_type)

        with tiledb.SparseArray(self.tile_uri, mode='w') as A:
            A[keys] = {'em': data}

        # print("write done")

    def get_data(self, key_list):
        data = None

        with tiledb.open(self.tile_uri, 'r') as A:
            # import pdb; pdb.set_trace()
            data = A.multi_index[key_list]['em']

        # print('read done')    
        return data
        


    