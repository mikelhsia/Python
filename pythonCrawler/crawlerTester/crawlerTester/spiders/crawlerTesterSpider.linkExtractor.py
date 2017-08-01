# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlertesterspiderSpider(CrawlSpider):
	name = 'crawlerTesterSpider'
	allowed_domains = ['comic.kukudm.com']
	start_urls = ['http://comic.kukudm.com/']

	rules = (
		Rule(LinkExtractor(allow=r'com'), callback='parse_item', follow=True, ),
		# Extract links matching 'category.php' (but not matching 'subsection.php')
		# and follow links from them (since no callback means follow=True by default).
		Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

		# Extract links matching 'item.php' and parse them with the spider's method parse_item
		Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
	)

	def parse_item(self, response):
		i = {}
		print "[Parse_item]: ", response.url
		# i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
		# i['name'] = response.xpath('//div[@id="name"]').extract()
		# i['description'] = response.xpath('//div[@id="description"]').extract()

		# self.logger.info('Hi, this is an item page! %s', response.url)
		# item = scrapy.Item()
		# item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
		# item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
		# item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		# return item
		return i

	# If the parse function is enabled, then it would replace "parse_item" function and "parse_item" won't run
	###################################
	# def parse(self, response):
	# 	print "[Parse]: ", response.url
