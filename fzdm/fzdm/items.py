# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FzdmItem(scrapy.Item):
	# 您可以为每个字段指明任何类型的元数据。 Field 对象对接受的值没有任何限制。
	# 也正是因为这个原因，文档也无法提供所有可用的元数据的键(key)参考列表

    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    mhurl = scrapy.Field()
    mhss = scrapy.Field()

    # 需要注意的是，用来声明item的 Field 对象并没有被赋值为class的属性。 
    # 不过您可以通过 Item.fields 属性进行访问。
