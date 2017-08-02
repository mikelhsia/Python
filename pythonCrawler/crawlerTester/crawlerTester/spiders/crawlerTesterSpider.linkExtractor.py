# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# from scrapy.exceptions import DropItem, CloseSpider, DontCloseSpider, IgnoreRequest, NotConfigured, NotSupported



class CrawlertesterspiderSpider(CrawlSpider):
	name = 'crawlerTesterSpider'
	allowed_domains = ['comic.kukudm.com']
	start_urls = ['http://comic.kukudm.com/']

	"""
		- Populating the settings -
		Settings can be populated using different mechanisms, each of which having a different precedence.Here is the
		list of them in decreasing order of precedence:
			- Command line options(most precedence)
			- Settings per-spider
			- Project settings module
			- Default settings per-command
			- Default global settings (less precedence)
	"""

	# Setting log file while running spider
	# scrapy crawl myspider - s LOG_FILE = scrapy.log

	# Setting per spider
	# custom_settings = {
	# 	'SOME_SETTING': 'some value',
	# }

	rules = (
		Rule(LinkExtractor(allow=r'com'), callback='parse_item', follow=True, ),
		# Rule(LinkExtractor(allow=r'com', tags=['img', 'a'], attrs='src', process_value=process_url), callback='parse_item', follow=True, ),

		# Extract links matching 'category.php' (but not matching 'subsection.php')
		# and follow links from them (since no callback means follow=True by default).
		# Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

		# Extract links matching 'item.php' and parse them with the spider's method parse_item
		# Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
	)

	def parse_item(self, response):
		i = {}
		self.logger.info("[Parse_item]: %s" % response.url)

		# How to access the settings
		# print("Existing settings: %s" % self.settings.attributes.keys())

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

	def process_url(self):
		pass

