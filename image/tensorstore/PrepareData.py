from torchvision.datasets import CIFAR100
import torchvision.transforms as tt
import constants

class PrepareData():

    def __init__(self):    
        stats = ((0.5074,0.4867,0.4411),(0.2011,0.1987,0.2025))

        train_transform = tt.Compose([
            tt.RandomHorizontalFlip(),
            tt.RandomCrop(32,padding=4,padding_mode="reflect"),
            tt.ToTensor(),
            tt.Normalize(*stats)
        ])

        self.input_data = CIFAR100(download=True,root = constants.PATH_TO_DATASET,transform=train_transform)

    def getInputData(self):
        return self.input_data
