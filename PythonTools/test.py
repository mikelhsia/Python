import timehutSeleniumToolKit as tstk
import timehutDataSchema

import unittest

import pdb
pdb.set_trace()


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
        # self.isHeadless = False
        self.timehut = tstk.timehutSeleniumToolKit(True, self.isHeadless)
        timehutUrl = "https://www.shiguangxiaowu.cn/zh-CN"

        self.timehut.fetchTimehutPage(timehutUrl)

        x = self.timehut.loginTimehut('mikelhsia@hotmail.com', 'f19811128')
        print(f'log in result: {x}')
        # if not self.timehut.loginTimehut('mikelhsia@hotmail.com', 'f19811128'):
        #     return False

        # print('Done setting up for the test')

    def test_a_run(self):
        print('\n### Testing behavior of scrolling down to trigger ajax call to get more content')

        req_list = self.timehut.getTimehutRecordedCollectionRequest()
        res_list = self.timehut.replayTimehutRecordedCollectionRequest(req_list)
        self.timehut.cleanTimehutRecordedCollectionRequest()

        collection_list = []
        for res in res_list:
            collection_list.append(parseCollectionBody(res))

        print(collection_list)

        self.assertEqual(0, 0)  # 测试用例


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
