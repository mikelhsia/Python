import requests
import json
import sys
import os
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import InternalError

import timehutDataSchema
import timehutManageLastUpdate
import timehutLog
import timehutSeleniumToolKit

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"


def check_rabbit_exist():
    rabbit_result = ''
    timehutLog.logging.info(f'Checking RabbitMQ ... ')
    with os.popen(RABBITMQ_PS_CMD, "r") as f:
        rabbit_result = f.read()

    f.close()

    return False if not rabbit_result else True


if __name__ == "__main__":
    if check_rabbit_exist():
        timehutLog.logging.info(f'RabbitMQ is running ... ')
    else:
        sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first")
        timehutLog.logging.error(f'Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first')
        sys.exit(1)

    '''
    lauch_receiver_worker()

    main_logic_with_sending_to_queue()
    '''
