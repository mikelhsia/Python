import timehutSeleniumToolKit as tstk
import timehutDataSchema

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import InternalError

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
            return False
        self.timehut.whereami('logged in')
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
        print('\n### Testing behavior of fetching collection')
        collection_list = self.timehut.getTimehutCollection()

        # print(collection_list)

        c_rec = timehutDataSchema.Collection(id=collection_list[0][0],
                                             baby_id=collection_list[0][1],
                                             created_at=collection_list[0][2],
                                             updated_at=collection_list[0][3],
                                             months=collection_list[0][4],
                                             days=collection_list[0][5],
                                             content_type=collection_list[0][6],
                                             caption=collection_list[0][7])
        print(c_rec)

        self.assertNotEqual(0, len(collection_list))  # 测试用例


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
