# -*- coding: utf-8 -*-
import scrapy
import urlparse
import os
import urllib

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

	def parse(self, response):
		# Use the text to find the right chapter
		print "Start Parsing"
		_xpathStr = "//a[contains(text(), \' %s%s\') and @target]/@href" % (self._targetChap, u'\u8bdd')
		_currentChap = response.xpath(_xpathStr).extract()
		self.logger.debug("[DEBUG] Inner url = %s", _currentChap)

		# TODO: Parse the entire URL to loop through those URL in different chapters

		itemUrl = u"http://comic.kukudm.com%s" % _currentChap[0]
		self.logger.debug("[DEBUG] itemUrl = %s", itemUrl)

		# TODO: Loop the 'targetChap' for 'numChap' times
		yield Request(url=itemUrl, callback=self.parse_item, dont_filter=True)

	def parse_item(self, response):
		item = KukuComicItem()

		# Parse filename and file source
		infoScript = response.xpath('//script/text()').extract()
		self.logger.debug("[DEBUG] Script = %s", infoScript)
		for line in infoScript:
			startStr = 'd+"'
			endStr = 'jpg'
			startIdx = line.find(startStr)
			endIdx = line.find(endStr)
			if startIdx > 0:
				item['imgSrc'] = self._comicServer + urllib.quote(line[startIdx+3:endIdx+3].encode("utf-8"))
				item['imgFileName'] = item['imgSrc'].split("/")[-1]
				self.logger.debug('[DEBUG] Source = %s', item['imgSrc'])
				break

		# TODO: Rename the folder name and downloaded filename
		dirName = response.xpath("/html/body/table[2]/tr/td[1]/text()").extract()
		for line in dirName:
			# self.logger.debug("[DEBUG] DIR = %s", line)
			deliIdx = line.find(' ')
			deliEndIdx = line.find(u'\u8bdd')
			item['imgDst'] = "%s/%s" % (os.getcwd(), self._targetChap)

		############################################################
		# 第一页的漫画只有一个list item，所以这个是nextlink
		# response.xpath("/html/body/table[2]/tr/td/a[1]/@href").extract()
		# 但是第二页之后的页面有两个link，所以第二个才是nextlink；有可能包含最后一页的链接
		# response.xpath("/html/body/table[2]/tr/td/a[2]/@href").extract()
		# 最后一页是这个链接: '/exit/exit.htm'
		############################################################
		try:
			next_link = response.xpath("/html/body/table[2]/tr/td/a[2]/@href").extract()
			self.logger.debug("[TESTING]: Next link - %s", next_link)
			if '/exit/exit.htm' not in next_link:
				self.logger.debug("[TESTING]: not exit.htm")
				# Meaning this is not the last page
				if not next_link:
					# Meaning this is the first page, so using the first link xpath instead of the second one
					next_link = response.xpath("/html/body/table[2]/tr/td/a[1]/@href").extract()[0]
					# self.logger.debug("[TESTING]: Next link url - %s", next_link)
					# self.logger.debug("[TESTING]: Response url - %s", response.url)
					# self.logger.debug("[TESTING]: Final url - %s", urlparse.urljoin(response.url, next_link))
				else:
					next_link = next_link[0]
					# self.logger.debug("[TESTING]: Next Link is not empty")
					# self.logger.debug("[TESTING]: Next link url - %s", next_link)
					# self.logger.debug("[TESTING]: Response url - %s", response.url)
					# self.logger.debug("[TESTING]: Final url - %s", urlparse.urljoin(response.url, next_link))
					pass
				yield Request(url=urlparse.urljoin(response.url, next_link), callback=self.parse_item, dont_filter=True)
			else:
				self.logger.debug("[TESTING]:exit.htm")
				pass

		except:
			self.logger.error("[TESTING]: Something went wrong")
			pass

		yield item

