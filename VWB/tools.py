import json


def log_json(data, filename):
    '''Append data to filename'''
    with open('VWB/logs/' + filename, 'a') as log_file:
        json.dump(data, log_file, indent=2, ensure_ascii=False)
        log_file.write('\n\n')