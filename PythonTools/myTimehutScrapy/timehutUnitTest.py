import timehutDataSchema
import timehutLog

import unittest
import sys
import os
# import pdb
# pdb.set_trace()

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"


def check_rabbit_exist():
    rabbit_result = ''
    timehutLog.logging.info(f'Checking RabbitMQ ... ')
    with os.popen(RABBITMQ_PS_CMD, "r") as f:
        rabbit_result = f.read()

    f.close()

    if not rabbit_result:
        return False

    return True

class MyTest(unittest.TestCase):  # 继承unittest.TestCase
    @classmethod
    def tearDownClass(cls):
        # 必须使用@classmethod 装饰器, 所有test运行完后运行一次
        print('End Timehut testing')
        print('----------------------------------')

    @classmethod
    def setUpClass(cls):
        # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('----------------------------------')
        if check_rabbit_exist():
            timehutLog.logging.info(f'RabbitMQ is running ... ')
        else:
            sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first")
            timehutLog.logging.error(f'Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first')
            sys.exit(1)
        print('Start Timehut testing')

    def tearDown(self):
        # 每个测试用例执行之后做操作
        # print('Tearing down the test env ...')
        print('Done tearing down the test env')

    def setUp(self):
        # 每个测试用例执行之前做操作
        # print('Setting up for the test ...')
        print('Done setting up for the test')

    def insert_to_queue(self):
        # print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        self.assertEqual(0, 0)  # 测试用例

    def fetch_from_queue(self):
        # print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        self.assertEqual(0, 0)  # 测试用例

    def insert_to_db(self):
        # print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        self.assertEqual(0, 0)  # 测试用例

    def delete_to_db(self):
        # print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        self.assertEqual(0, 0)  # 测试用例


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
