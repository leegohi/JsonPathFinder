import json
import ast

def load_json(json_str:str)->dict:
    try:
        return json.loads(json_str)
    except:
        return ast.literal_eval(json_str)