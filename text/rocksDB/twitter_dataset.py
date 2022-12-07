'''
    @brief: Data format for twitter dataset
    @prereq: bash
    @usage: 
    @authors: Benita, Hemal, Reetuparna
'''

import json

class TwitterDataset:
    def __init__(self, target, ids, date, flag, user, text):
        self.target = target
        self.ids = ids
        self.date = date
        self.flag = flag
        self.user = user
        self.text = text
   
    # convert data members to json
    def to_json(self):
        return json.dumps(self, indent = 4, default=lambda o: o.__dict__)