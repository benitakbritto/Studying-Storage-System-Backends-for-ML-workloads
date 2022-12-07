'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

from torchvision.datasets import CIFAR100
import torchvision.transforms as tt

class PrepareData():

    def __init__(self, input_path):    
        stats = ((0.5074,0.4867,0.4411),(0.2011,0.1987,0.2025))

        train_transform = tt.Compose([
            tt.RandomHorizontalFlip(),
            tt.RandomCrop(32,padding=4,padding_mode="reflect"),
            tt.ToTensor(),
            tt.Normalize(*stats)
        ])

        self.input_data = CIFAR100(download=True, root = input_path, transform=train_transform)

    def getInputData(self):
        return self.input_data
