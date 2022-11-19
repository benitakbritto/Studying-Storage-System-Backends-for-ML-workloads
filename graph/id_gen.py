import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import string

'''
Usage:
    vertex_id_gen = IdGen()

    def get_id(val):
        return vertex_id_gen.get(val) 
'''

class IdGen:
    def __init__(self):
        self.id = multiprocessing.Value('i', 0)
        self.dict = dict()

    def get(self, str):
        with self.id.get_lock():
            # put if it does not exist
            if str not in self.dict:
                self.dict[str] = self.id.value
                # advance to the next id
                self.id.value += 1
            
            return self.dict[str]


if __name__ == "__main__":
    idgen = IdGen()

    def get_id(str):
        return (str,idgen.get(str))    
    
    tasks = []

    strs = string.ascii_lowercase[:26]

    with ProcessPoolExecutor(max_workers=8) as executor:
            
        for i in strs:
            task = executor.submit(get_id, *[i])
            tasks.append(task)

    print("Task results: ", [t.result() for t in tasks])