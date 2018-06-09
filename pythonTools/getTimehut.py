import requests
import logging
import json

import timehutDataSchema

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(filename='log1.log',
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)

memoryCollectionSet = set()
memorySet = set()

# functions
def getRequest(baby_id, before_day):
    headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cookie': 'locale=en;user_session=BAhJIj1qcF81MzY5MjMzNjNfM0JyZDJlNV9LbkJ1OGtqdkRqSHM4UmZyVk1CVUk4a3BrY1JRME9ZVzc1dwY6BkVU--fcb138d8ae1fcb3290cbbd7c4b35101f61d8b40e'
    }

    try:
        r = requests.get(url='http://peekaboomoments.com/events.json?baby_id={}&before={}&v=2&width=700&include_rt=true'.format(baby_id, before_day), headers=headers, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        print(e)
        logging.error(e)
    else:
        response_body = json.loads(r.text)
        print("Request fired = {}".format(response_body['next']))
        logging.info("Request fired = {}".format(response_body['next']))
        return response_body['next'], response_body

def parseResponseBody(response_body):
    pass

def createEngine(dbName, loggingFlag):
    engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306', echo=loggingFlag)
    #engine = create_engine('mysql+pymysql://root:michael0512@127.0.0.1:3306', echo=loggingFlag)

    engine.execute("CREATE DATABASE IF NOT EXISTS {}".format(dbName))
    print("CREATE DATABASE IF NOT EXISTS {}".format(dbName))
    logging.info("CREATE DATABASE IF NOT EXISTS {}".format(dbName))

    engine.execute("USE {}".format(dbName))
    print("USE {}".format(dbName))
    logging.info("USE {}".format(dbName))


# main function()
def main():
    __before_day = -200
    __baby_id = 537413380
    __next_index = 0
    __dbName = "peekaboo" 
    __logging = False
    __engine = createEngine(__dbName, __logging)

    while (True):
        __next_index, __response_body = getRequest(__baby_id, __before_day)

        parseResponseBody(__response_body)

        if (__next_index is None):
            break

        __before_day = __next_index + 1


# check
if __name__ == "__main__":
    main()
