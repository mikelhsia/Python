1
"""
This extension is a simple extension to illustrate the concepts described in the previous section. 
This extension will log a message every time:
- a spider is opened
- a spider is closed
- a specific number of items are scraped.

For more information: https://doc.scrapy.org/en/latest/topics/extensions.html

Settings:
The extension will be enabled through the MYEXT_ENABLED setting and the number 
of items will be specified through the MYEXT_ITEMCOUNT setting.
"""

import logging

from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class SpiderOpenCloseLogging(object):
	def __init__(self, item_count):
		self.item_count = item_count
		self.item_scraped = 0

	@classmethod
	def from_crawler(cls, crawler):
		# first check if the extension should be enabled and raise
		# NotConfigured otherwise
		if not crawler.settings.getbool('MYEXT_ENABLED'):
			raise NotConfigured

		# get the number of items from settings
		item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

		# instantiate the extension object
		ext = cls(item_count)

		# connect the extension object to signals
		crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
		crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
		crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

		# Return the ext object
		return ext

	def spider_opened(self, spider):
		logging.info("[MyExt] opened spider %s", spider.name)
		pass

	def spider_closed(self, spider):
		logging.info("[MyExt] closed spider %s", spider.name)
		pass

	def item_scraped(self, item, spider):
		self.items_scraped += 1
		if self.items_scraped % self.item_count == 0:
			logger.info("[MyExt] scraped %d items", self.items_scraped)
