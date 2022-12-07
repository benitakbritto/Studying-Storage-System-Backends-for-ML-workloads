import tiledb
import numpy as np

class Embeddings:
    def __init__(self, entries_count, embedding_len, uri):
        self.enties_count = entries_count
        self.embedding_len = embedding_len
        self.uri = uri

        # store value as tuple(em[0], em[1]..., em[len-1])
        self.np_tuple_type =  ','.join('f4' for _ in range(0, embedding_len))

        self.__create_tiledb_schema__(entries_count=entries_count, uri=uri)
    
    def __create_tiledb_schema__(self, entries_count, uri):
        # Create the dimension, inclusive of both end
        d1 = tiledb.Dim(domain=(0, entries_count - 1), tile=2, dtype=np.int32)

        # Create a domain using the dimension
        dom = tiledb.Domain(d1)

        # Create a dummy attr, required
        # np_tuple_type = ','.join('f4' for _ in range(0, cols_count))
        em_attr = tiledb.Attr(name="em", dtype=np.dtype(self.np_tuple_type))

        # Create the array schema, setting `sparse=False` to indicate a dense array
        schema = tiledb.ArraySchema(domain=dom, attrs=[em_attr])

        tiledb.DenseArray.create(uri, schema, overwrite=True)

        print('TileDB schema created')

    def get(self, idx):
        with tiledb.open(self.uri, 'r') as A:
            return A[idx]

    def put(self, idx, np_arr):
        # convert to tuple of embedding_len
        data = np.array([tuple(row) for row in np_arr], dtype=self.np_tuple_type)

        with tiledb.DenseArray(self.uri, mode='w') as A:
            A[idx] = {'em': data}
        


    