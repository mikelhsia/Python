# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider

'''
该spider除了其按行遍历而不是节点之外其他和XMLFeedSpider十分类似。
而其在每次迭代时调用的是 parse_row() 。
'''
class FzdmCsvfeedSpider(CSVFeedSpider):
    name = 'fzdm-csvfeed'
    allowed_domains = ['http://manhua.fzdm.com/']
    start_urls = ['http://http://manhua.fzdm.com//feed.csv']
    # headers = ['id', 'name', 'description', 'image_link']
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        i = {}
        #i['url'] = row['url']
        #i['name'] = row['name']
        #i['description'] = row['description']
        return i

'''
Example:

from scrapy import log
from scrapy.contrib.spiders import CSVFeedSpider
from myproject.items import TestItem

class MySpider(CSVFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    headers = ['id', 'name', 'description']

    def parse_row(self, response, row):
        log.msg('Hi, this is a row!: %r' % row)

        item = TestItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']
        return item
'''