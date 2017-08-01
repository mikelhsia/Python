# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlertesterspiderSpider(CrawlSpider):
	name = 'crawlerTesterSpider'
	allowed_domains = ['http://comic.kukudm.com/']
	start_urls = ['http://comic.kukudm.com/']

	rules = (
		Rule(LinkExtractor(allow=r'index'), callback='parse_item', follow=True, ),
	)

	def parse_item(self, response):
		i = {}
		print response.url
		# i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
		# i['name'] = response.xpath('//div[@id="name"]').extract()
		# i['description'] = response.xpath('//div[@id="description"]').extract()
		return i