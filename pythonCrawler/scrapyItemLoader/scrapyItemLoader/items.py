# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Scrapy的Item是进行数据保存不可缺少的步骤，
# 通过它进行数据的整理并通过Pipelines进行数据的数据库保存，图片下载等，
# 它只有一种类型scrapy.Field()。
# 由于需要添加一个封面图，对上面的爬虫添加一个front_image_url字段对parse函数进行修改

class ScrapyitemloaderItem(scrapy.Item):
	# chapNum  = scrapy.Field()
	imgFileName = scrapy.Field()
	imgSrc = scrapy.Field()
	imgDst = scrapy.Field()
	pass
