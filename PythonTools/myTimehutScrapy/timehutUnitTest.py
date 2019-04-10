import pika
import sys

import unittest
import sys
import json
import os

import timehutManageDB as TMDB
# import pdb
# pdb.set_trace()

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"
RABBIT_SERVICE_DEV_URL = 'localhost'
TIMEHUT_RABBITMQ_QUEUE_NAME = 'timehut_queue'

mock_collection = '''
{
    "list": [
        {
            "id": 698622945853968493,
            "id_str": "698622945853968493",
            "baby_id": 537413380,
            "taken_at_gmt": 1554768325,
            "months": 36,
            "days": 1,
            "active": true,
            "auto_generated": true,
            "auto_layout": true,
            "updated_at": "2019-04-09T00:26:25.950Z",
            "updated_at_in_ts": 1554769585.950565,
            "layout": "collection",
            "layout_detail": [
                {
                    "id": 698623001529159795,
                    "id_str": "698623001529159795",
                    "type": "picture",
                    "content": null,
                    "taken_at_gmt": 1554768325,
                    "service": null,
                    "picture": "https://alicn.timehutcdn.cn/sz/pictures/original/201904/537810747/2191570BDD254AFC9D21D8D2D2CA37FA.jpg",
                    "picture_width": 3024,
                    "picture_height": 4032,
                    "parent_id": null,
                    "event_id": 698622945853968493,
                    "baby_id": 537413380,
                    "event_caption": null
                },
                {
                    "id": 698622991508967538,
                    "id_str": "698622991508967538",
                    "type": "picture",
                    "content": null,
                    "taken_at_gmt": 1554768336,
                    "service": null,
                    "picture": "https://alicn.timehutcdn.cn/sz/pictures/original/201904/537810747/DC388DE7DFAE48A396D1C0E5381DA76E.jpg",
                    "picture_width": 3024,
                    "picture_height": 4032,
                    "parent_id": null,
                    "event_id": 698622945853968493,
                    "baby_id": 537413380,
                    "event_caption": null
                },
                {
                    "id": 698622945925271663,
                    "id_str": "698622945925271663",
                    "type": "picture",
                    "content": null,
                    "taken_at_gmt": 1554768337,
                    "service": null,
                    "picture": "https://alicn.timehutcdn.cn/sz/pictures/original/201904/537810747/805E5AEB626C406C8785A3C2282ECBAA.jpg",
                    "picture_width": 3024,
                    "picture_height": 4032,
                    "parent_id": null,
                    "event_id": 698622945853968493,
                    "baby_id": 537413380,
                    "event_caption": null
                }
            ],
            "relations": "mom",
            "counts": {
                "comments": 0,
                "likes": 0,
                "texts": 0,
                "pictures": 5,
                "videos": 0,
                "audios": 0,
                "red_likes": 0,
                "rich_texts": 0,
                "stars": 0
            },
            "caption": null,
            "like": false,
            "red_like": false
        },
    ],
    "next": 1096,
    "reverse": false
}
'''

mock_moment='''
{
    "id": 665864717089116986,
    "id_str": "665864717089116986",
    "baby_id": 537413380,
    "taken_at_gmt": 1546848391,
    "months": 32,
    "days": 30,
    "active": true,
    "auto_generated": true,
    "auto_layout": true,
    "updated_at": "2019-03-12T12:38:21.775Z",
    "updated_at_in_ts": 1552394301.775257,
    "layout": "collection",
    "layout_detail": null,
    "relations": "mom,dad",
    "counts": {
        "comments": 0,
        "likes": 0,
        "texts": 0,
        "pictures": 20,
        "videos": 1,
        "audios": 0,
        "red_likes": 0,
        "rich_texts": 0,
        "stars": 3
    },
    "caption": "早上醒來不到10分鐘就出門了，今天爸爸找到新方法吸引讓他刷牙了：捉蟲蟲 哈哈。",
    "like": false,
    "red_like": false,
    "moments": [
        {
            "id": 668572549056040984,
            "id_str": "668572549056040984",
            "event_id": 665864717089116986,
            "event_id_str": "665864717089116986",
            "baby_id": 537413380,
            "user_id": 537810747,
            "relation": "mom",
            "type": "picture",
            "content": null,
            "fields": null,
            "parent_id": null,
            "cover": null,
            "service": null,
            "picture": "https://alicn.timehutcdn.cn/sz/pictures/original/201901/537810747/E68D429EA5BB4BA6A864707FF3B31AD4.jpg",
            "picture_file_size": 883126,
            "picture_width": 3024,
            "picture_height": 4032,
            "privacy": "public",
            "active": true,
            "star": false,
            "taken_at_gmt": 1546848391,
            "months": 32,
            "days": 30,
            "client_id": "B845DDD6-503A-40C3-B308-A62F1FC032DA",
            "comments_count": 0,
            "likes_count": 0,
            "red_likes_count": 0,
            "created_at": "2019-01-16T02:16:39.774Z",
            "updated_at": "2019-01-16T02:16:39.774Z",
            "like": false,
            "red_like": false,
            "tagging_record": [],
            "tagging_records": []
        }
    ]
}
'''

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

    def test_rabbitMQ_publish_collection(self):
        print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        if check_rabbit_exist():
            sys.stdout.write(f'RabbitMQ is running ... \n')
        else:
            sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first\n")
            self.assertEqual(0, 1)  # 测试用例

        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVICE_DEV_URL))
        channel = connection.channel()
        channel.queue_declare(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, durable=True)

        message = {"type": "collection", "header": f"{mock_collection}", "request": 3}
        
        channel.basic_publish(exchange='', routing_key=TIMEHUT_RABBITMQ_QUEUE_NAME,
                              body=json.dumps(message).encode('UTF-8'),
                              properties=pika.BasicProperties(delivery_mode=2,
                                                              content_type='application/json',
                                                              content_encoding='UTF-8'))

        print(f' [x] Message sent')
        connection.close()
        # check_db()
        # delete_to_db()
        self.assertEqual(0, 0)  # 测试用例

    def test_rabbitMQ_publish_moment(self):
        print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        if check_rabbit_exist():
            sys.stdout.write(f'RabbitMQ is running ... \n')
        else:
            sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first\n")
            self.assertEqual(0, 1)  # 测试用例

        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVICE_DEV_URL))
        channel = connection.channel()
        channel.queue_declare(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, durable=True)

        message = {"type":"moment", "header": f"{mock_moment}", "request": 3}

        channel.basic_publish(exchange='', routing_key=TIMEHUT_RABBITMQ_QUEUE_NAME,
                              body=json.dumps(message).encode('UTF-8'),
                              properties=pika.BasicProperties(delivery_mode=2,
                                                              content_type='application/json',
                                                              content_encoding='UTF-8'))

        print(f' [x] Message sent')
        connection.close()
        # check_db()
        # delete_to_db()
        self.assertEqual(0, 0)  # 测试用例


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
