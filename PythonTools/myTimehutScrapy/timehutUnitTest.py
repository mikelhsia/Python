import pika
import sys

import unittest
import sys
import json
import os
# import pdb
# pdb.set_trace()

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"
RABBIT_SERVICE_DEV_URL = 'localhost'
TIMEHUT_RABBITMQ_QUEUE_NAME = 'timehut_queue'


def check_rabbit_exist():
    rabbit_result = ''
    sys.stdout.write(f'Checking RabbitMQ ... \n')
    with os.popen(RABBITMQ_PS_CMD, "r") as f:
        rabbit_result = f.read()
    f.close()

    return False if not rabbit_result else True

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
        print('Start Timehut testing')

    def tearDown(self):
        # 每个测试用例执行之后做操作
        # print('Tearing down the test env ...')
        print('Done tearing down the test env')

    def setUp(self):
        # 每个测试用例执行之前做操作
        # print('Setting up for the test ...')

        print('Done setting up for the test')

    def test_rabbitMQ_publish(self):
        print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        if check_rabbit_exist():
            sys.stdout.write(f'RabbitMQ is running ... \n')
        else:
            sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first\n")
            self.assertEqual(0, 1)  # 测试用例

        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVICE_DEV_URL))
        channel = connection.channel()
        channel.queue_declare(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, durable=True)


        message = {"header": "Test", "request": 3}
        
        
        channel.basic_publish(exchange='', routing_key=TIMEHUT_RABBITMQ_QUEUE_NAME,
                              body=json.dumps(message).encode('UTF-8'),
                              properties=pika.BasicProperties(delivery_mode=2, content_type='application/json', content_encoding='UTF-8'))

        print(f' [x] Message sent')
        connection.close()
        # publish_task()
        # insert_to_db()
        # delete_to_db()
        self.assertEqual(0, 0)  # 测试用例


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
