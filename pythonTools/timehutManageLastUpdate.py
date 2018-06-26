import os
from pathlib import Path

last_update_ts_path = Path().absolute()

last_update_ts_file = f'{last_update_ts_path}/timehutLastUpdatedTimestamp.file'

def readLastUpdateTimeStamp():
    try:
        with open(last_update_ts_file, 'r+') as f:
            ts = f.read()
            return ts
    except FileNotFoundError as e:
        print(f'File {last_update_ts_file} not found, creating a new file')
        os.system(f'touch {last_update_ts_file}') 
        print(f'File {last_update_ts_file} created.')

def writeLastUpdateTimeStamp(timestamp):
    with open(last_update_ts_file, 'w') as f:
        f.write(str(timestamp))
    print(f'Update last updated timestamp in file {last_update_ts_file}')

