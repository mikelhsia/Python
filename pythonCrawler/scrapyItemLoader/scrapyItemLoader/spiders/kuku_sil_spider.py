# -*- coding: utf-8 -*-
import scrapy
# This is for python
# import urlparse
# This is for python3
from urllib.parse import urljoin
import os
import urllib

# Selenium getting ajax url
from selenium import webdriver
from selenium.webdriver.common.by import By as WebCommonBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as WebExpectedCond

from scrapy import signals
from scrapy.http import Request
from scrapyItemLoader.items import KukuComicItem


driver = ""

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
		crawler.signals.connect(spider.spider_opened, signal=scrapy.signals.spider_opened)
		crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
		return spider

	def spider_opened(self, spider):
		# Selenium chrome web driver
		global driver
		driver = webdriver.PhantomJS()

		spider.logger.info('Spider opened signal received, and webdriver PhantomJS is opened')

	def spider_closed(self, spider):
		# Close the driver
		global driver
		driver.close()
		del driver

		spider.logger.info('Spider closed signal received, and webdriver PhantomJS is closed')

	def parse(self, response):
		for num in range(0, int(self._numChap)):
			# Notes regarding Xpath:
			#  - Disable Firefox Javascript while inspecting the DOM looking for XPaths to be used in Scrapy
			#  - Never use full XPath paths, use relative and clever ones based on attributes (such as id, class,
			# width, etc) or any identifying features like contains(@href, 'image').
			#  - Never include <tbody> elements in your XPath expressions unless you really know what you’re doing

			# Use the text to find the right chapter
			# _xpathStr = "//a[contains(text(), \' %s%s\') and @target]/@href" % (str(int(self._targetChap)+num), u'\u8bdd')
			_xpathStr = "//a[contains(text(), %s) and @target]/@href" % (str(int(self._targetChap)+num))
			# self.logger.debug("[DEBUG] xpath = %s", _xpathStr)
			_currentChap = response.xpath(_xpathStr).extract()
			if not _currentChap:
				print(_currentChap)
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

		driver.get(response.url)
		## Make sure fetching element won't take too long and die silently
		# http://selenium-python.readthedocs.io/waits.html
		#################################################################################
		# This waits up to 5 seconds before throwing a TimeoutException unless it finds the element
		# to return within 5 seconds. WebDriverWait by default calls the ExpectedCondition every
		# 500 milliseconds until it returns successfully. A successful return is for ExpectedCondition type is Boolean return true or not null return value for all other ExpectedCondition types.
		try:
			element = WebDriverWait(driver, 5).until(
				# WebExpectedCond.presence_of_element_located((WebCommonBy.ID, "myDynamicElement"))
				WebExpectedCond.presence_of_element_located((WebCommonBy.XPATH, "/html/body/table[2]/tbody/tr/td/img"))
			)
		except:
			self.logger.ERROR("[ERROR] Source = {}".format("PhantomJS not getting the element"))
		finally:
			img_url = element.get_attribute("src")

		# img_url = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/img").get_attribute("src")
		self.logger.debug("[DEBUG] Source = {}".format(img_url))

		item['imgSrc'] = img_url
		item['imgFileName'] = img_url.split("/")[-1]

		# Rename the folder name and downloaded filename
		item['imgDst'] = "%s/%s/%s" % (os.getcwd(), response.url.split('/')[-2], response.url.split('/')[-1].replace('htm', 'jpg'))
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
				yield Request(url=urljoin(response.url, next_link), callback=self.parse_item, dont_filter=True)
			else:
				self.logger.debug("Hit /exit.htm")
				pass

		except Exception as e:
			self.logger.error("Something went wrong: {}".format(e))
			pass

		yield item

