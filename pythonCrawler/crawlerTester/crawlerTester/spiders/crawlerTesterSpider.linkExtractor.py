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
	)

	def parse_item(self, response):
		i = {}
		print "[Parse_item]: ", response.url
		# i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
		# i['name'] = response.xpath('//div[@id="name"]').extract()
		# i['description'] = response.xpath('//div[@id="description"]').extract()
		return i

	# If the parse function is enabled, then it would replace "parse_item" function and "parse_item" won't run
	###################################
	# def parse(self, response):
	# 	print "[Parse]: ", response.url
