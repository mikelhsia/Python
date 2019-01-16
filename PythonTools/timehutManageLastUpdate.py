import os
import timehutLog
from pathlib import Path

last_update_ts_path = Path().absolute()
last_update_ts_file = f'{last_update_ts_path}/timehutLastUpdatedTimestamp.file'

class LastUpdateTsManager(object):
    __last_update_ts_onon = 0
    __last_update_ts_muimui = 0

    def __init__(self):
        try:
            with open(last_update_ts_file, 'r+') as f:
                ts = f.read()
                ts = ts.split(f',') 
                self.__last_update_ts_muimui = float(ts[1])
                self.__last_update_ts_onon = float(ts[0])
        except FileNotFoundError as e:
            timehutLog.logging.info(f'File {last_update_ts_file} not found, creating a new file')
            os.system(f'echo \"0,0\" > {last_update_ts_file}') 
            timehutLog.logging.info(f'File {last_update_ts_file} created.')

            self.__last_update_ts_onon = 0
            self.__last_update_ts_muimui = 0

    def readLastUpdateTimeStamp(self, baby_id):
        if baby_id == 537776076:
            # Mui Mui Baby ID
            return self.__last_update_ts_muimui
        else:
            # On on Baby ID
            return self.__last_update_ts_onon

    def writeLastUpdateTimeStamp(self, timestamp, baby_id):
        try:
            with open(last_update_ts_file, 'w') as f:
                if baby_id == 537776076: 
                    # Mui mui Baby ID updated
                    self.__last_update_ts_muimui = timestamp
                else:
                    # On on Baby ID updated
                    self.__last_update_ts_onon = timestamp
                f.write(f'{self.__last_update_ts_onon},{self.__last_update_ts_muimui}')
        except Exception as e:
            raise e
        finally:
            timehutLog.logging.info(f'Update last updated timestamp in file {last_update_ts_file}')

