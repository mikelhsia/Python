# -*- coding: utf-8 -*-
import scrapy
import urlparse
import os

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
	comicServer = 'http://n.1whour.com/'

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
		# TODO: 除了用链接title之外，还可以用其他方法，例如去list里的第几个等等...
		# Use the text to find the right chapter
		_xpathStr = "//a[contains(text(), \' %s%s\') and @target]/@href" % (self._targetChap, u'\u8bdd')
		x = response.xpath(_xpathStr).extract()
		self.logger.info("[TESTING]: %s", x)

		yield Request(url=response.url, callback=self.parse_detail, dont_filter=True)

	def parse_detail(self, response):
		item = KukuComicItem()

		infoScript = response.xpath('//script[@type="text/javascript"]/text()').extract()
		for line in infoScript:
			startStr = 'var mhurl = "'
			endStr = 'jpg'
			startIdx = line.find(startStr)
			endIdx = line.find(endStr)
			if startIdx > 0:
				item['imgFileName'] = line[startIdx+13:endIdx+3]
				break

		if (item['imgFileName'].find('2015') != -1 or item['imgFileName'].find('2016') != -1 or item['imgFileName'].find('2017') != -1):
			item['imgSrc'] = "http://%s/%s" % (u"p1.xiaoshidi.net", item['imgFileName'])
		else:
			item['imgSrc'] = "http://%s/%s" % (u"s1.nb-pintai.com", item['imgFileName'])

		item['imgFileName'] = item['imgFileName'].replace('/','-')
		item['imgDst'] = "%s/%s" % (os.getcwd(), response.url.split("/")[-2])

		try:
			next_link = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract().pop()
			#  /exit/exit.htm
			# / html / body / table[2] / tbody / tr / td / a[4]

			if next_link:
				yield Request(url=urlparse.urljoin(response.url, next_link), callback=self.parse, dont_filter=True)
		except:
			pass

