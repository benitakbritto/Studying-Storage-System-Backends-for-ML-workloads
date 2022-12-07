import tensorstore as ts
from csv import reader
import tensor.twitter_dataset as twitter
from tensor.helper import int_to_bytes
import tensor.constants

class TSStore:
    def __init__(self, input_file):
        self.db = ts.KvStore.open({'driver': 'memory'}).result()
        self.input_file = input_file

    async def ingestData(self):
        row_index = 0
        with open(self.input_file, 'r', encoding=tensor.constants.INPUT_FILE_ENCODING) as read_obj:
            
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
                key = int_to_bytes(row_index)
                val = json_string.encode()
                
                # write to tensorstore
                await self.db.write(key, val)

                row_index += 1  
            
        self.len = row_index
        