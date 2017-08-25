# -*- coding: utf-8 -*-
import scrapy
import urlparse
import os
import urllib

from scrapy import signals
from scrapy.http import Request
from scrapyItemLoader.items import KukuComicItem

class SilSpiderSpider(scrapy.Spider):
	name = 'kuku_sil_spider'
	allowed_domains = ['comic.kukudm.com']
	start_urls = []

	# serverList
	# - m200911d = 'http://n.1whour.com/'
	# - m201001d = 'http://n.1whour.com/'
	# - m201304d = 'http://n.1whour.com/'
	_comicServer = 'http://n.1whour.com/'

	_manga = 1
	_targetChap = 1
	_numChap = 1

	def __init__(self, manga=1, targetChap=1, numChap=1, *args, **kwargs):
		super(SilSpiderSpider, self).__init__(*args, **kwargs)
		self._manga = manga
		self._targetChap = targetChap
		self._numChap = numChap
		# self.log("[%s, %s, %s]" % (manga, targetChap, numChap))
		self.start_urls = ["http://comic.kukudm.com/comiclist/%s/index.htm" % self._manga]

	# Implementation of signals interception in spider
	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(SilSpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		spider.logger.info('Spider closed: %s', spider.name)

	def parse(self, response):
		for num in range(0, int(self._numChap)):
			# Notes regarding Xpath:
			#  - Disable Firefox Javascript while inspecting the DOM looking for XPaths to be used in Scrapy
			#  - Never use full XPath paths, use relative and clever ones based on attributes (such as id, class,
			# width, etc) or any identifying features like contains(@href, 'image').
			#  - Never include <tbody> elements in your XPath expressions unless you really know what you’re doing

			# Use the text to find the right chapter
			_xpathStr = "//a[contains(text(), \' %s%s\') and @target]/@href" % (str(int(self._targetChap)+num), u'\u8bdd')
			# self.logger.debug("[DEBUG] xpath = %s", _xpathStr)
			_currentChap = response.xpath(_xpathStr).extract()
			if not _currentChap:
				self.logger.info("[INFO] No further comic")
				break
			itemUrl = u"http://comic.kukudm.com%s" % _currentChap[0]

			# self.logger.debug("[DEBUG] itemUrl = %s", itemUrl)
			#################################################################################
			# The return of parse function link to pipeline - process_request() function which
			# - If None
			#       Do nothing
			# - If Response
			#       Put the response to scheduler and parse it again
			# - If Item
			#       parse the item
			#################################################################################
			yield Request(url=itemUrl, callback=self.parse_item, dont_filter=True)

	def parse_item(self, response):
		item = KukuComicItem()

		# parse filename and file source
		infoScript = response.xpath('//script/text()').extract()
		# self.logger.debug("[DEBUG] Script = %s", infoScript)
		for line in infoScript:
			startStr = 'd+"'
			endStr = 'jpg'
			startIdx = line.find(startStr)
			endIdx = line.find(endStr)
			if startIdx > 0:
				item['imgSrc'] = self._comicServer + urllib.quote(line[startIdx+3:endIdx+3].encode("utf-8"))
				item['imgFileName'] = item['imgSrc'].split("/")[-1]
				# self.logger.debug('[DEBUG] Source = %s', item['imgSrc'])
				break

		# Rename the folder name and downloaded filename
		item['imgDst'] = "%s/%s/%s" % (os.getcwd(), response.url.split('/')[-2], response.url.split('/')[-1].replace('htm', 'jpg')
)
		# self.logger.debug("[DEBUG] Dst folder = %s", item['imgDst'])
		############################################################
		# 第一页的漫画只有一个list item，所以这个是nextlink
		# response.xpath("/html/body/table[2]/tr/td/a[1]/@href").extract()
		# 但是第二页之后的页面有两个link，所以第二个才是nextlink；有可能包含最后一页的链接
		# response.xpath("/html/body/table[2]/tr/td/a[2]/@href").extract()
		# 最后一页是这个链接: '/exit/exit.htm'
		############################################################
		try:
			next_link = response.xpath("/html/body/table[2]/tr/td/a[2]/@href").extract()
			if '/exit/exit.htm' not in next_link:
				# Meaning this is not the last page
				if not next_link:
					# Meaning this is the first page, so using the first link xpath instead of the second one
					next_link = response.xpath("/html/body/table[2]/tr/td/a[1]/@href").extract()[0]
				else:
					next_link = next_link[0]
					pass
				yield Request(url=urlparse.urljoin(response.url, next_link), callback=self.parse_item, dont_filter=True)
			else:
				self.logger.debug("Hit /exit.htm")
				pass

		except:
			self.logger.error("Something went wrong")
			pass

		yield item

