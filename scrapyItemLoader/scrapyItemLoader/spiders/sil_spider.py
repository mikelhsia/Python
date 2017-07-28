# -*- coding: utf-8 -*-
import scrapy
import urlparse
import os

from scrapyItemLoader.items import ScrapyitemloaderItem
from scrapy.http import Request

class SilSpiderSpider(scrapy.Spider):
	name = 'sil_spider'
	allowed_domains = ["manhua.fzdm.com/"]

	manga      = int(raw_input("食戟之靈 - 58\t七原罪 - 56\n猎人 - 10\t东京RE - 117\n进击 - 39\t英雄学院 - 131\nInput Manga code: "))
	targetChap = int(raw_input("Input start downloading chapter: "))
	numChap    = int(raw_input("How many chapters you want to download: "))

	start_urls = ["http://manhua.fzdm.com/%d/%d/" % (manga, chap) for chap in xrange(targetChap, targetChap+numChap)]
	# for x in range(numChap):
	# 	start_urls.append("http://manhua.fzdm.com/%d/%d/" % (manga, targetChap+x))
	# 	print "http://manhua.fzdm.com/%d/%d/" % (manga, targetChap+x)

	def parse(self, response):
		# meta字段是传递值的方法。在调试时返回的response中会出现meta的内容，它是一个字典，
		# 故在传递时可以直接通过 response.meta['front_image_url']进行引用
		# (也可以使用get的方法，附默认值防止出现异常）
		# 加了dont_filter=True的参数就完全可以用了！Why!?
		# self.log("1. [URL Parsing and Downloading Image]: %s" % response.url)
		yield Request(url=response.url, callback=self.parse_detail, dont_filter=True)

		## We want to inspect one specific response
		# 您可以点击Ctrl-D(Windows下Ctrl-Z)来退出终端
		# 注意: 由于该终端屏蔽了Scrapy引擎，您在这个终端中不能使用 fetch 快捷命令(shortcut)。 
		# 当您离开终端时，spider会从其停下的地方恢复爬取，正如上面显示的那样。
		#############################################
		# scrapy.shell.inspect_response(response, self)

		try:
			next_link = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract().pop()
			# self.log("2. [URL Parsing - Next link]: %s" % next_link)

			if next_link:
				# self.log("3. [URL Parsing - Goes to next link]: %s" % next_link)
				yield Request(url=urlparse.urljoin(response.url, next_link), callback=self.parse, dont_filter=True)
				# 注：可以修改settings.py 中的配置文件，以此来指定“递归”的层数，如： DEPTH_LIMIT = 1
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

