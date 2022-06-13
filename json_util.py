import json


def json_read(file):
    read_json_file = open(file, 'r')
    json_data = json.load(read_json_file)
    read_json_file.close()
    return json_data


def json_write(file, data):
    write_json = json.dumps(data, indent=4)
    write_file = open(file, 'w')
    write_file.write(write_json)
    write_file.close()
    return
