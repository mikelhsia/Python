# -*- coding: utf-8 -*-
import scrapy
import urlparse
import os

from scrapy.http import Request

class SilSpiderSpider(scrapy.Spider):
	name = 'kuku_sil_spider'
	allowed_domains = ['comic.kukudm.com']

	# manga      = int(raw_input("食戟之靈 - 58\t七原罪 - 56\t辛巴达 - 119\n"
	#                            "猎人 - 10\t东京RE - 117\n"
	#                            "进击 - 39\t英雄学院 - 131"
	#                            "\nInput Manga code: "))
	# targetChap = int(raw_input("Input start downloading chapter: "))
	# numChap    = int(raw_input("How many chapters you want to download: "))

	start_urls = []

	def __init__(self, manga=1, targetChap=1, numChap=1, *args, **kwargs):
		super(SilSpiderSpider, self).__init__(*args, **kwargs)
		self.start_urls = ["http://comic.kukudm.com/comiclist/2049/index.htm"]
		self.log("[%s, %s, %s]" % (manga, targetChap, numChap))

	def parse(self, response):

		# self.log("1. [URL Parsing and Downloading Image]: %s" % response.url)
		yield Request(url=response.url, callback=self.parse_detail, dont_filter=True)

		try:
			next_link = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract().pop()
			# self.log("2. [URL Parsing - Next link]: %s" % next_link)

			if next_link:
				# self.log("3. [URL Parsing - Goes to next link]: %s" % next_link)
				yield Request(url=urlparse.urljoin(response.url, next_link), callback=self.parse, dont_filter=True)
		except:
			# self.log("4. [URL Parsing]: Nothing to be poped")
			pass

	def parse_detail(self, response):
		item = ScrapyitemloaderItem()

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

		yield item

