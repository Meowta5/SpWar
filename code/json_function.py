import json

def write(data, path):
    '''Изменяет данные json'''
    data = json.dumps(data)
    data = json.loads(str(data))
    
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3)

def read(path):
    '''Загружает данные json'''
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

