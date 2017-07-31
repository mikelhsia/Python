# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider


class FzdmXmlfeedSpider(XMLFeedSpider):

    '''
    XMLFeedSpider被设计用于通过迭代各个节点来分析XML源(XML feed)。 
    迭代器可以从 iternode, xml, html 选择。鉴于 xml 以及 html 迭代器需要先
    读取所有DOM再分析而引起的性能问题，一般还是推荐使用 iternodes。
    不过使用 html 作为迭代器能有效应对错误的XML。
    '''
    name = 'fzdm-xmlfeed'
    allowed_domains = ['http://manhua.fzdm.com/']
    start_urls = ['http://http://manhua.fzdm.com//feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = {}
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return i

'''
Example:

from scrapy import log
from scrapy.contrib.spiders import XMLFeedSpider
from myproject.items import TestItem

class MySpider(XMLFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.xml']
    iterator = 'iternodes' # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        log.msg('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.extract())))

        item = TestItem()
        item['id'] = node.xpath('@id').extract()
        item['name'] = node.xpath('name').extract()
        item['description'] = node.xpath('description').extract()
        return item

简单来说，我们在这里创建了一个spider，从给定的 start_urls 中下载feed， 
并迭代feed中每个 item 标签，输出，并在 Item 中存储有些随机数据。

'''