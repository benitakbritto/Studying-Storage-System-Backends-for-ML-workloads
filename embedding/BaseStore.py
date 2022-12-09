class BaseStore():
    def __init__(self):
        pass

    def get_data(self, key_list):
        NotImplementedError("should be implemented in child class")
    
    def store_data(self, key_list, value_list):
        NotImplementedError("should be implemented in child class")