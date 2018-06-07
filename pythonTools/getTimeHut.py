import requests
import json

import getTimehutData

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# functions
def getRequest(baby_id, before_day):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cookie': 'locale=en;user_session=BAhJIj1qcF81MzY5MjMzNjNfM0JyZDJlNV9LbkJ1OGtqdkRqSHM4UmZyVk1CVUk4a3BrY1JRME9ZVzc1dwY6BkVU--fcb138d8ae1fcb3290cbbd7c4b35101f61d8b40e'
    }

    r = requests.get(url='http://peekaboomoments.com/events.json?baby_id={}&before={}&v=2&width=700&include_rt=true'.format(baby_id, before_day), headers=headers)

    response_body = json.loads(r.text)
#    print(response_body)
    print("Request fired = {}".format(response_body['next']))
    return response_body['next']

def createEngine():
    engine = create_engine('mysql+pymysql://root:michael0512@127.0.0.1:3306/php_test')


# main function()
def main():
    before_day = 50
    baby_id = 537413380
    next_index = 0
    while (next_index is not None):
        before_day = next_index + 2
        nex_index = getRequest(baby_id, before_day)
#    createEngine()
    getTimehutData.printabc()

# check
if __name__ == "__main__":
    main()
