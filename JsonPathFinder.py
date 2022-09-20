from typing import List
from copy import deepcopy
import sys
from clip import get_clip
from json_loader import load_json

class JsonPathFinder:
    def __init__(self, json_str, mode='key'):
        self.data = load_json(json_str) 
        self.mode = mode

    def iter_node(self, rows, road_step, target):
        if isinstance(rows, dict):
            key_value_iter = (x for x in rows.items())
        elif isinstance(rows, list):
            key_value_iter = (x for x in enumerate(rows))
        else:
            return
        for key, value in key_value_iter:
            current_path = road_step.copy()
            current_path.append(key)
            if self.mode == 'key':
                check = key
            else:
                check = value
            if check == target:
                yield current_path
            if isinstance(value, (dict, list)):
                yield from self.iter_node(value, current_path, target)

    def find_one(self, target: str) -> list:
        path_iter = self.iter_node(self.data, [], target)
        for path in path_iter:
            return path
        return []

    def find_all(self, target) -> List[list]:
        path_iter = self.iter_node(self.data, [], target)
        return list(path_iter)
    def get_val(self,path):
        value=self.data
        for step in path:
            value = value[step]
        return deepcopy(value)
    def find_val(self,target):
        path=self.find_one(target)
        return [path,self.get_val(path)]
    def find_all_val(self,target):
        paths=self.find_all(target)
        vals=[]
        for path in paths:
            val=self.get_val(path)
            vals.append([path,val])
        return vals
def main():
    if len(sys.argv)==2:
        with open(sys.argv[1], ) as f:
            json_data = f.read()
    else:
        json_data=get_clip()
    finder = JsonPathFinder(json_data)
    key=input("输入json关键字key:")
    all_val=finder.find_all_val(key)
    for index,val in  enumerate(all_val):
        print(index,val[0],"\n",val[1])
if __name__ == '__main__':
   main()