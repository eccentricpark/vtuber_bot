import json


def read_json_file(file='../../mao.json'):
    with open(file, "r", encoding='UTF8') as f:
        data = json.load(f)      
    return data