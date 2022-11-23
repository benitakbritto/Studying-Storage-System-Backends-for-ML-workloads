import tensorstore as ts
import constants

class TensorStoreDB():

    def __init__(self):
        self.db = ts.KvStore.open({'driver': 'memory', 'path': constants.KVSTORE_PATH}).result()

