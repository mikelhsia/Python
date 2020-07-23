# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import os
import urllib
from tqdm import tqdm

# Selenium getting ajax url
from selenium import webdriver
from selenium.webdriver.common.by import By as WebCommonBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as WebExpectedCond

from scrapy import signals
from scrapy.http import Request
from scrapyItemLoader.items import KukuComicItem


driver = ""
CHROMEDRIVER_PATH = "../chromedriver"

class SilSpiderSpider(scrapy.Spider):
	name = 'kuku_sil_spider'
	allowed_domains = ['comic2.kukudm.com']
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
		self.start_urls = ["http://comic2.kukudm.com/comiclist/%s/index.htm" % self._manga]

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
		# driver = webdriver.PhantomJS(executable_path="/Users/puppylpy/Python/pythonCrawler/phantomjs")
		option = webdriver.ChromeOptions()
		option.add_argument('--headless')
		driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=option)
		spider.logger.info('Spider opened signal received, and webdriver PhantomJS is opened')

	def spider_closed(self, spider):
		# Close the driver
		global driver
		driver.close()
		del driver

		spider.logger.info('Spider closed signal received, and webdriver PhantomJS is closed')

	def parse(self, response):
		# Notes regarding Xpath:
		#  - Disable Firefox Javascript while inspecting the DOM looking for XPaths to be used in Scrapy
		#  - Never use full XPath paths, use relative and clever ones based on attributes (such as id, class,
		# width, etc) or any identifying features like contains(@href, 'image').
		#  - Never include <tbody> elements in your XPath expressions unless you really know what you’re doing

		if not self._numChap:
			numChap = 1
		else:
			numChap = int(self._numChap)

		if not self._targetChap:
			targetChap = 1
		else:
			targetChap = int(self._targetChap) - 1

		# Use the text to find the right chapter
		_xpathStr = f"//dd/a[1]/@href"
		# self.logger.debug("[DEBUG] xpath = %s", _xpathStr)
		_currentChap = response.xpath(_xpathStr).extract()

		if not _currentChap:
			# print(_currentChap)
			self.logger.info("[INFO] No further comic")
			return

		_currentChap = _currentChap[targetChap:targetChap + numChap]

		# print("*****************")
		# print(f"URL: {response.url}")
		# print(f"Response: {response.body}")
		# print(f'Xpath = {_xpathStr}')
		# print(f'Num of current = {len(_currentChap)}')
		# print("Current = ", _currentChap)
		# print("Current = ", _currentChap)
		# print("*****************")

		#################################################################################
		# The return of parse function link to pipeline - process_request() function which
		# - If None
		#       Do nothing
		# - If Response
		#       Put the response to scheduler and parse it again
		# - If Item
		#       parse the item
		#################################################################################
		for c in tqdm(_currentChap):
			# self.logger.debug("[DEBUG] itemUrl = %s", itemUrl)
			itemUrl = u"http://comic2.kukudm.com%s" % _currentChap[0]
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
				WebExpectedCond.presence_of_element_located((WebCommonBy.XPATH, "/html/body/table[2]/tbody/tr/td/a[1]/img"))
			)
		except:
			self.logger.ERROR("[ERROR] Source = {}".format("PhantomJS not getting the element"))
		finally:
			img_url = element.get_attribute("src")

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
			next_link = response.xpath("//a[last()]/@href").extract()[0]
			if '/exit/exit.htm' not in next_link:
				# Meaning this is not the last page
				yield Request(url=urljoin(response.url, next_link), callback=self.parse_item, dont_filter=True)
			else:
				self.logger.debug("Hit /exit.htm")

		except Exception as e:
			self.logger.error("Something went wrong: {}".format(e))

		yield item

