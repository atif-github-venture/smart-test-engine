import json


def write_json(content, path):
    with open(path, 'w') as f:
        json.dump(content, f)
        f.close()


def read_json_data(path):
    with open(path) as json_file:
        return json.load(json_file)
