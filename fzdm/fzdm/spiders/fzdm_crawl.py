# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FzdmCrawlSpider(CrawlSpider):
    name = 'fzdm-crawl'
    allowed_domains = ['http://manhua.fzdm.com/']
    start_urls = ['http://http://manhua.fzdm.com//']

    '''
    爬取规则(Crawling rules)
        class scrapy.contrib.spiders.Rule(link_extractor, callback=None, 
                                        cb_kwargs=None, follow=None, 
                                        process_links=None, process_request=None) 

        link_extractor 
            是一个 Link Extractor 对象。 其定义了如何从爬取到的页面提取链接。

        callback 
            是一个callable或string(该spider中同名的函数将会被调用)。
            从link_extractor中每获取到链接时将会调用该函数。
            该回调函数接受一个response作为其第一个参数，并返回一个包含 Item 以及(或) 
            Request 对象(或者这两者的子类)的列表(list)。
    
        !警告!
            当编写爬虫规则时，请避免使用 parse 作为回调函数。 由于 CrawlSpider 使用 parse 方法来实现其逻辑，如果 您覆盖了 parse 方法，crawl spider 将会运行失败。
        
        cb_kwargs 
            包含传递给回调函数的参数(keyword argument)的字典。

        follow 
            是一个布尔(boolean)值，指定了根据该规则从response提取的链接是否需要跟进。 
            如果 callback 为None， follow 默认设置为 True ，否则默认为 False 。

        process_links 
            是一个callable或string(该spider中同名的函数将会被调用)。 
            从link_extractor中获取到链接列表时将会调用该函数。该方法主要用来过滤。

        process_request 
            是一个callable或string(该spider中同名的函数将会被调用)。 
            该规则提取到每个request时都会调用该函数。该函数必须返回一个request或者None。 
            (用来过滤request)
    '''
    
    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
