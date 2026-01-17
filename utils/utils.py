import json

def read_json_file(file_path):
    """Reads a JSON file and returns its content as a dictionary."""

    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    """Writes a dictionary to a JSON file."""

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4) 