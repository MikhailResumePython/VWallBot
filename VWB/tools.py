import json
from VWB import vk, tg_methods as tg
import datetime
import sys, os

def log_json(data, filename):
    '''Append json data to filename'''
    with open(f'VWB/logs/{filename}', 'a') as log_file:
        json.dump(data, log_file, indent=2, ensure_ascii=False)
        log_file.write('\n\n')


def log_err(text, filename):
    '''Append error data to filename'''
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    with open(f'VWB/logs/{filename}', 'a') as log_file:
        log_file.write(str(datetime.datetime.now()))
        log_file.write(f'\n{text} {exc_type} {fname} {exc_tb.tb_lineno}\n\n')


def init_tokens(filename):
    ''' Initialize API tokens'''
    with open(filename, 'r') as token_file:
        tg.BOT_TOKEN = token_file.readline()[:-1]
        vk.VK_ACCESS_TOKEN = token_file.readline()
        
        