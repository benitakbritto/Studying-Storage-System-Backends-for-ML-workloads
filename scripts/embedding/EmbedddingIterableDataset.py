from torch.utils.data import IterableDataset

class EmbedddingIterableDataset(IterableDataset):
    def __init__(self, path):
        #Store the filename in object's memory
        self.path = path

    def __preprocess(self, line):
        line = line.strip('\n')
        return int(line)

    def __iter__(self):
        #Create an iterator
        file_itr = open(self.path)

        mapped_itr = map(self.__preprocess, file_itr)

        return mapped_itr