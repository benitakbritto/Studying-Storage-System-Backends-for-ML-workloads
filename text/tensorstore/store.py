from csv import reader
import constants
import twitter_dataset as twitter
import tensorstore as ts
import asyncio
import time
import json

class TensorStoreLoader:

    async def initialize(self):
        self.store = await ts.KvStore.open({'driver': 'memory'}) 
        print("Store init done")

    # TODO: Extract out to common helper for all text types
    def int_to_bytes(self, num):
        str_val = str(num)
        return str_val.encode()

    async def getData(self):
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

    async def read_from_db(self, key):
        print('Reading ', key)
        key_in_bytes = None
        if isinstance(key, int):
            key_in_bytes = self.int_to_bytes(key)
        elif isinstance(key, str):
            key_in_bytes = key.encode()

        print('key_in_bytes ', key_in_bytes)
        val = await self.store.read(key_in_bytes)
        assert val is not None

        print('val ', val.value)  

'''
    Driver
'''

if __name__ == "__main__":
    loader = TensorStoreLoader()

    # TODO: Cleanup / find an alternative way
    
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(loader.initialize())
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    print("start at ", time.time())
    tasks = [
        loop.create_task(loader.getData())
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    print("end at ", time.time())

    tasks = [
        loop.create_task(loader.read_from_db(10))
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    loop.close()