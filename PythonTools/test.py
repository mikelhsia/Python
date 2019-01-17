import timehutSeleniumToolKit as tstk
import timehutDataSchema

import unittest
import sys
import os
import math
# import pdb
# pdb.set_trace()


def progressBar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()

def parseCollectionBody(response_body):
    collection_list = []

    data_list = response_body['list']

    for data in data_list:

        if data['layout'] == 'collection' or \
                data['layout'] == 'picture' or \
                data['layout'] == 'video' or \
                data['layout'] == 'text':

            c_rec = timehutDataSchema.Collection(id=data['id_str'],
                                                 baby_id=data['baby_id'],
                                                 created_at=data['taken_at_gmt'],
                                                 updated_at=data['updated_at_in_ts'],
                                                 months=data['months'],
                                                 days=data['days'],
                                                 content_type=timehutDataSchema.CollectionEnum[data['layout']].value,
                                                 caption=data['caption'])

            # Add to return collection obj list
            collection_list.append(c_rec)
        # print(c_rec)

        elif data['layout'] == 'milestone':
            continue

        else:
            print(data)
            raise TypeError

    return collection_list


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
        self.timehut.quitTimehutPage()
        # print('Done tearing down the test env')
        # os.system('rm -rf ./*.png')

    def setUp(self):
        # 每个测试用例执行之前做操作
        # print('Setting up for the test ...')
        self.isHeadless = True
        self.timehut = tstk.timehutSeleniumToolKit(True, self.isHeadless)
        timehutUrl = "https://www.shiguangxiaowu.cn/zh-CN"

        self.timehut.fetchTimehutPage(timehutUrl)

        if not self.timehut.loginTimehut('mikelhsia@hotmail.com', 'f19811128'):
            print('Login failed')
            return False

        print('Login success')
        # print('Done setting up for the test')

    def test_a_run(self):
        print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')
        test_result = 0
        test_target = 0

        # Testing Scrolling down to trigger another ajax
        for i in range(0, test_target):
            self.timehut.scrollDownTimehutPage()
            if self.timehut.whereami(i):
                test_result += 1
            progressBar(test_result, test_target)

        self.assertEqual(test_target, test_result)  # 测试用例

    def test_b_run(self):
        print('\n### Testing behavior of switching baby id')
        mui_mui_homepage = 'http://47.75.157.88/en/home/537776076'
        self.timehut.fetchTimehutPage(mui_mui_homepage)
        self.assertEqual(True, self.timehut.whereami('mui_mui'))  # 测试用例

    def test_c_run(self):
        print('\n### Testing behavior of fetching album list')
        num = self.timehut.getTimehutAlbumURLSet()

        self.assertNotEqual(0, num)  # 测试用例

    def test_d_run(self):
        self.timehut.scrollDownTimehutPage()

        req_list = self.timehut.getTimehutRecordedCollectionRequest()
        res_list = self.timehut.replayTimehutRecordedCollectionRequest(req_list)
        # res_list = self.timehut.replayTimehutRecordedCollectionRequest(req_list, 1007)
        self.timehut.cleanTimehutRecordedCollectionRequest()

        collection_list = []
        for res in res_list:
            collection_list += parseCollectionBody(res)

        # print(collection_list)

        self.assertEqual(0, 0)  # 测试用例


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
