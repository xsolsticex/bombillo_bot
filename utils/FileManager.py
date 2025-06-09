import os

import json


class FileManager:
    def __init__(self):
        self.file_path = "./data/tokens.json"

    
    def file_exists(self):
        if os.path.exists(self.file_path):
            return True
        return False
    
    def write_file(self,data:dict):
        with open(self.file_path,"w") as file:
            json.dump(data,file,indent=4)

    def read_file(self):
        with open(self.file_path,"r") as file:
            data = json.load(file)
        return data