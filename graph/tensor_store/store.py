'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import tensorstore as ts
import tensor_store.constants as constants
from tensor_store.helper import int_to_bytes, convert_tensor_to_bytes

class TSStore():

    def __init__(self, input_path):
        self.db = ts.KvStore.open({'driver': 'memory', 'path': constants.KVSTORE_PATH}).result()
        self.input_path = input_path

    async def ingestData(self):
        row_index = 0

        with open(self.input_path, 'r') as file:
            for line in file:
                key_in_bytes = int_to_bytes(row_index)
                val_in_bytes = convert_tensor_to_bytes(line)
                await self.db.write(key_in_bytes, val_in_bytes)
                row_index += 1
                
            self.num_rows = row_index