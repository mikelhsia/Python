#!/usr/local/bin/python
#! -*- coding: UTF-8 -*-

'''
对spider来说，爬取的循环类似下文:

以初始的URL初始化Request，并设置回调函数。 
当该request下载完毕并返回时，将生成response，并作为参数传给该回调函数。
spider中初始的request是通过调用 start_requests() 来获取的。 
start_requests() 读取 start_urls 中的URL， 并以 parse 为回调函数生成 Request 。
在回调函数内分析返回的(网页)内容，返回 Item 对象或者 Request 或者一个包括二者的可迭代容器。 
返回的Request对象之后会经过Scrapy处理，下载相应的内容，并调用设置的callback函数(函数可相同)。
在回调函数内，您可以使用 选择器(Selectors) (您也可以使用BeautifulSoup, lxml 或者您想用的任何解析器) 
来分析网页内容，并根据分析的数据生成item。
最后，由spider返回的item将被存到数据库(由某些 Item Pipeline 处理)或使用 Feed exports 存入到文件中。
'''

'''
为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义以下三个属性:
1. name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
2. start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 
   后续的URL则从初始的URL获取到的数据中提取。
3. parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 
   该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
'''
import scrapy
import os
import sys
import urllib
import time

from fzdm.items import FzdmItem
# from scrapy.http import Request

class fzdmSpider(scrapy.Spider):
	# 必须定义name，即爬虫名，如果没有name，会报错。因为源码中是定义为必须的。
	name = "fzdm"
	allowed_domains = ["manhua.fzdm.com/"]

	manga = int(raw_input("Input Manga code: "))
	targetChap = int(raw_input("Input start downloading chapter: "))
	numChap = int(raw_input("How many chapters you want to download: "))

	# Scrapy为Spider的 start_urls 属性中的每个URL创建了 scrapy.Request 对象，
	# 并将 parse 方法作为回调函数(callback)赋值给了Request。
	start_urls = []
	for x in range(numChap):
		start_urls.append("http://manhua.fzdm.com/%d/%d/index.html" % (manga, targetChap+x))
		# print "http://manhua.fzdm.com/%d/%d/index.html" % (manga, targetChap+x)

		for y in range(22):
			start_urls.append("http://manhua.fzdm.com/%d/%d/index_%d.html" % (manga, targetChap+x, y+1))
			# print "http://manhua.fzdm.com/%d/%d/index_%d.html" % (manga, targetChap+x, y+1)


	def parse(self, response):
		# Selector有四个基本的方法(点击相应的方法可以看到详细的API文档):
		# - xpath(): 传入xpath表达式，返回该表达式所对应的所有节点的selector list列表 。
		#   -- /html/head/title: 选择HTML文档中 <head> 标签内的 <title> 元素
		# 	-- /html/head/title/text(): 选择上面提到的 <title> 元素的文字
		# 	-- //td: 选择所有的 <td> 元素
		# 	-- //div[@class="mine"]: 选择所有具有 class="mine" 属性的 div 元素
		# article	选取所有article元素的所有子节点
		# /article	选取根元素article
		# article/a	选取所有属于article的子元素的a元素
		# //div	选取所有div元素（不管出现在文档里的任何地方）
		# article//div	选取所有属于article元素的后代的div元素，不管它出现在article之下的任何位置
		# //@class	选取所有名为class的属性
		# /article/div[1]	选取属于article子元素的第一个div元素
		# /article/div[last()]	选取属于article子元素的最后一个div元素
		# /article/div[last()-1]	选取属于article子元素的倒数第二个div元素
		# //div[@lang]	选取所有拥有lang属性的div元素
		# //div[@lang='eng']	选取所有lang属性值为eng的div元素
		# /div/*	选取属于div元素的所有子节点
		# //*	选取所有元素
		# //div[@*]	选取所有带属性的div 元素
		# //div/a 丨//div/p	选取所有div元素的a和p元素
		# //span丨//ul	选取文档中的span和ul元素
		# article/div/p丨//span	选取所有属于article元素的div元素的p元素以及文档中所有的 span元素
		##################
		# - css(): 传入CSS表达式，返回该表达式所对应的所有节点的selector list列表.
		# *	选择所有节点
		# #container	选择id为container的节点
		# .container	选择所有class包含container的节点
		# li a	选取所有li下的所有a节点
		# ul + p	选择ul后面的第一个p元素
		# div#container > ul	选取id为container的div的第一个ul子元素
		# ul ~ p	选取与ul相邻的所有p元素
		# a[title]	选取所有有title属性的a元素
		# a[href="http://163.com"]	选取所有href属性为163的a元素
		# a[href*="163"]	选取所有href属性包含163的a元素
		# a[href^="http"]	选取所有href属性以http开头的a元素
		# a[href$=".jpg"]	选取所有href以.jpg结尾的a元素
		# input[type=radio]:checked	选择选中的radio的元素
		# div:not(#container)	选取所有id非container的div属性
		# li:nth-child(3)	选取第三个li元素
		# tr:nth-child(2n)	第偶数个tr
		##################
		# - extract(): 序列化该节点为unicode字符串并返回list。
		# - re(): 根据传入的正则表达式对数据进行提取，返回unicode字符串list列表。
		#########################################
		# class scrapy.selector.Selector(response=None, text=None, type=None)
		#########################################
		# Selector 的实例是对选择某些内容响应的封装。
		# response 是 HtmlResponse 或 XmlResponse 的一个对象，将被用来选择和提取数据。
		#
		# text 是在 response 不可用时的一个unicode字符串或utf-8编码的文字。将 text 和 response 一起使用是未定义行为。
		# 
		# type 定义了选择器类型，可以是 "html", "xml" or None (默认).
		# 	如果 type 是 None ，选择器会根据 response 类型(参见下面)自动选择最佳的类型，或者在和 text 一起使用时，默认为 "html" 。
		# 	如果 type 是 None ，并传递了一个 response ，选择器类型将从response类型中推导如下：
		# 		"html" for HtmlResponse type
		# 		"xml" for XmlResponse type
		# 		"html" for anything else
		# 	其他情况下，如果设定了 type ，选择器类型将被强制设定，而不进行检测。

		item = FzdmItem()
		item['name'] = response.xpath('//title/text()').extract()
		# Servers url that store images before 2015
		item['mhss'] = u's1.nb-pintai.com'
		item['mhurl'] = response.xpath('//script[@type="text/javascript"]/text()').extract()

		for line in item['mhurl']:
			startStr = 'var mhurl = "'
			endStr = 'jpg'
			startIdx = line.find(startStr)
			endIdx = line.find(endStr)
			if startIdx > 0:
				# self.log(line[startIdx+13:endIdx+3])
				# self.log("[Found]!")
				item['mhurl'] = line[startIdx+13:endIdx+3]
				break

		# Servers url that store images after 2015
		if (item['mhurl'].find('2015') != -1 or item['mhurl'].find('2016') != -1 or item['mhurl'].find('2017') != -1):
			item['mhss'] = u'p1.xiaoshidi.net'

		# Creating all the folder and file necessary
		# filename = response.url.split("/")[-1]
		src = "http://%s/%s" % (item['mhss'],item['mhurl'])
		fileName = item['mhurl'].replace('/','-')
		dirName = response.url.split("/")[-2]
		filePath = "%s/%s" % (os.getcwd(), dirName)
		dst = os.path.join(filePath, fileName)

		try:
			os.mkdir(dirName)
		except:
			# self.log("[IOError]: folder is already exist!")
			pass

		urllib.urlretrieve(src, dst)
		
		# 怕太频繁的要求会被挡IP, has been achieved in the setting.py
		# DOWNLOAD_DELAY = 0.25
		# time.sleep(0.3)

		return item


'''
下载档案
ab_src = "http://www.xiaohuar.com" + src[0]#相对路径拼接
file_name = "%s_%s.jpg" % (school[0].encode('utf-8'), name[0].encode('utf-8')) #文件名，因为python27默认编码格式是unicode编码，因此我们需要编码成utf-8
file_path = os.path.join("/Users/wupeiqi/PycharmProjects/beauty/pic", file_name)
urllib.urlretrieve(ab_src, file_path)
注：urllib.urlretrieve(ab_src, file_path) ，接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径。
'''
