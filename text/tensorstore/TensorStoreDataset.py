import asyncio
import constants
import json
import twitter_dataset as twitter
import tensorstore as ts
import time
from csv import reader
from torch.utils.data import Dataset, DataLoader

class TensorStoreDataset(Dataset):

    def __init__(self):
        self.store = ts.KvStore.open({'driver': 'memory'}).result()
        print("Store init done")

    async def ingestData(self):
        row_index = 0
        with open(constants.DATASET_PATH, 'r') as read_obj:
            
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
                key = self.int_to_bytes(row_index)
                val = json_string.encode()
                
                # write to tensorstore
                await self.store.write(key, val)

                row_index += 1  
            
        self.len = row_index

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        val = self.store.read(self.int_to_bytes(idx)).result().value
        val = json.loads(val.decode())
        return val['text'], val['target']

    # TODO: Extract out to common helper for all text types
    def int_to_bytes(self, num):
        str_val = str(num)
        return str_val.encode()

'''
    Driver
'''

if __name__ == "__main__":
    dataset = TensorStoreDataset()

    # TODO: Cleanup / find an alternative way
    
    # Ingest data
    loop = asyncio.get_event_loop()
    start = time.time()
    tasks = [
        loop.create_task(dataset.ingestData())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end = time.time()
    print(f'Elapsed time in ingestion = {end - start}')

    # Load data
    start = time.time()    
    
    # TODO: Tweak these values
    data_train = DataLoader(
        dataset,
        batch_size=4,
        shuffle=True, 
        num_workers=0
    )

    i = 0
    for batch_idx, samples in enumerate(data_train):
        i = batch_idx
    
    end = time.time()
    print(f'Elapsed time in loading = {end - start}')