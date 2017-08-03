# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

######################################################################################
from scrapy.mail import MailSender
mailer = MailSender()
# Or you can instantiate it passing a Scrapy settings object, which will respect the settings:
# mailer = MailSender.from_settings(settings)
# Below is how you send email
# mailer.send(to=["someone@example.com"], subject="Some subject", body="Some body", cc=["another@example.com"])
######################################################################################

# from scrapy.exceptions import DropItem, CloseSpider, DontCloseSpider, IgnoreRequest, NotConfigured, NotSupported

######################################################################################
# On top of that, you can create different “loggers” to encapsulate messages.
# (For example, a common practice is to create different loggers for every module).
# These loggers can be configured independently, and they allow hierarchical constructions.
######################################################################################
######################################################################################
# To get you started on manually configuring logging’s output, you can use logging.basicConfig()
# to set a basic root handler. This is an example on how to redirect INFO or higher messages to a file:
# import logging
# from scrapy.utils.log import configure_logging
# configure_logging(install_root_handler=False)
# logging.basicConfig(
#     filename='log.txt',
#     format='%(levelname)s: %(message)s',
#     level=logging.INFO
# )
######################################################################################
import logging
# logger = logging.getLogger("UseThisNotRoot")


class CrawlertesterspiderSpider(CrawlSpider):
	name = 'crawlerTesterSpider'
	allowed_domains = ['comic.kukudm.com']
	start_urls = ['http://comic.kukudm.com/']

	######################################################################################
	# - Populating the settings -
	# Settings can be populated using different mechanisms, each of which having a different precedence.Here is the
	# list of them in decreasing order of precedence:
	# 	- Command line options(most precedence)
	# 	- Settings per-spider
	# 	- Project settings module
	# 	- Default settings per-command
	# 	- Default global settings (less precedence)
	######################################################################################

	# Setting log file while running spider
	# scrapy crawl myspider - s LOG_FILE = scrapy.log

	# Setting per spider
	# custom_settings = {
	# 	'SOME_SETTING': 'some value',
	# }

	rules = (
		Rule(LinkExtractor(allow=r'index.htm'), callback='parse_item', follow=True, ),
		# Rule(LinkExtractor(allow=r'com', tags=['img', 'a'], attrs='src', process_value=process_url), callback='parse_item', follow=True, ),

		######################################################################################
		# Extract links matching 'category.php' (but not matching 'subsection.php')
		# and follow links from them (since no callback means follow=True by default).
		# Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

		# Extract links matching 'item.php' and parse them with the spider's method parse_item
		# Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
		######################################################################################
	)

	def __init__(self, *args, **kwargs):
		# If you run this spider again then INFO messages from scrapy.spidermiddlewares.httperror logger will be gone.
		logger = logging.getLogger("scrapy.middleware")
		logger.setLevel(logging.WARNING)
		super(CrawlertesterspiderSpider, self).__init__(*args, **kwargs)

	def parse_item(self, response):
		i = {}
		# Log as root logger
		# Scrapy provides a logger within each Spider instance, which can be accessed and used like this
		# Or Customize your spider logger's name as above
		self.logger.info("[Parse_item]: %s" % response.url)

		# Log by defined name
		logger = logging.getLogger("Michael_Hsia")
		logger.log(logging.WARNING, "[Parse_item]: End")

		# Log by Spider file name
		logger2 = logging.getLogger(__name__)
		logger2.log(logging.DEBUG, "[Parse_item]: ----------------")

		# How to access the settings
		# print("Existing settings: %s" % self.settings.attributes.keys())

		######################################################################################
		# self.logger.info('Hi, this is an item page! %s', response.url)
		# item = scrapy.Item()
		# item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
		# item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
		# item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		# return item
		######################################################################################
		return i

	######################################################################################
	# If the parse function is enabled, then it would replace "parse_item" function and "parse_item" won't run
	######################################################################################
	# def parse(self, response):
	# 	print "[Parse]: ", response.url

	# function for processing the url got from using tags and attributes
	def process_url(self):
		pass

