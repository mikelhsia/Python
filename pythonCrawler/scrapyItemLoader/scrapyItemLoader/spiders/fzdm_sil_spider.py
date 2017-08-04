# -*- coding: utf-8 -*-
import scrapy
import urlparse
import os
import logging

from scrapyItemLoader.items import ScrapyitemloaderItem
from scrapy.http import Request


class SilSpiderSpider(scrapy.Spider):
	name = 'sil_spider'
	allowed_domains = ["manhua.fzdm.com/"]
	start_urls = []

	def __init__(self, manga = 1, targetChap = 1, numChap = 1, *args, **kwargs):
		super(scrapy.Spider, self).__init__(*args, **kwargs)

		self.start_urls = ["http://manhua.fzdm.com/%s/%s/" % (int(manga), chap) for chap in xrange(int(targetChap), int(targetChap)+int(numChap))]
		# self.log(logging.INFO, "[%s, %s, %s]" % (manga, targetChap, numChap))

	def parse(self, response):
		# This is a contract for us
		""" This function parses a sample response. Some contracts are mingled with this docstring.

		@url http://manhua.fzdm.com/56/130/
		@returns requests 0 1
		"""
		###########################################################################
		# @url http://manhua.fzdm.com/56/130/     # 合同书，没有这个凭据就不会开始测试
		# @returns items 0 1                      # 最多或最少返回几个item
		# @returns requests 0 2                   # 最多或最少返回几个request
		# @scrapes imgSrc imgDst acbd             # 检查返回的Item里是否有定义的字段
		###########################################################################
		# Contracts Class
		# adjust_request_args(args)
		# This receives a dict as an argument containing default arguments
		# for Request object.Must return the same or a modified version of it.
		#
		# pre_process(response)
		# This allows hooking in various checks on the response received from the sample request,
		# before it’s being passed to the callback.
		#
		# post_process(output)
		# This allows processing the output of the callback.
		# Iterators are converted listified before being passed to this hook.
		###########################################################################
		# Example:
		# /usr/local/lib/python2.7/site-packages/scrapy/contracts/default.py
		# ------
		# from scrapy.contracts import Contract
		# from scrapy.exceptions import ContractFail
		#
		# class HasHeaderContract(Contract):
		# 	""" Demo contract which checks the presence of a custom header
		# 		@has_header X-CustomHeader
		# 	"""
		#
		# 	name = 'has_header'
		#
		# 	def pre_process(self, response):
		# 		for header in self.args:
		# 			if header not in response.headers:
		# 				raise ContractFail('X-CustomHeader not present')
		###########################################################################

		# meta字段是传递值的方法。在调试时返回的response中会出现meta的内容，它是一个字典，
		# 故在传递时可以直接通过 response.meta['front_image_url']进行引用
		# (也可以使用get的方法，附默认值防止出现异常）
		# 加了dont_filter=True的参数就完全可以用了！Why!?
		# self.log("1. [URL Parsing and Downloading Image]: %s" % response.url)
		yield Request(url=response.url,
		              callback=self.parse_detail,
		              dont_filter=True)

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
				yield Request(url=urlparse.urljoin(response.url, next_link),
				              callback=self.parse,
				              dont_filter=True)
				# 注：可以修改settings.py 中的配置文件，以此来指定“递归”的层数，如： DEPTH_LIMIT = 1
		except:
			# self.log("4. [URL Parsing]: Nothing to be poped")
			pass

	def parse_detail(self, response):
		""" This function parses a sample response. Some contracts are mingled with this docstring.

		@url http://manhua.fzdm.com/56/130/
		@returns items 0 16
		@scrapes imgSrc imgDst acbd
		"""
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

