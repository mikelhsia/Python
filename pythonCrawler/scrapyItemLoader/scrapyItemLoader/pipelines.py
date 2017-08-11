# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib
from scrapy.utils.trackref import get_oldest

class ScrapyitemloaderPipeline(object):

	def open_spider(self, spider):
		print """######################\n"
		"# Now we're about to awake the spider\n"
		"######################\n"""

	def process_item(self, item, spider):

		# Creating all the folder and file necessary
		# dst = os.path.join(item['imgDst'], item['imgFileName'])

		try:
			os.mkdir(os.path.split(item['imgDst'])[0])
		except:
			# self.logger.info("[INFO]: folder is already exist!")
			pass

		r = get_oldest('HtmlResponse')
		print get_oldest(r.url)

		urllib.urlretrieve(item['imgSrc'], item['imgDst'])
		return item


		######################################################################
		# This is Custom Images pipeline examples
		######################################################################
		# import scrapy
		# from scrapy.pipelines.images import ImagesPipeline
		# from scrapy.exceptions import DropItem
		#
		# class MyImagesPipeline(ImagesPipeline):
		#
		# 	def get_media_requests(self, item, info):
		# 		for image_url in item['image_urls']:
		# 			yield scrapy.Request(image_url)
		#
		# 	def item_completed(self, results, item, info):
		# 		image_paths = [x['path'] for ok, x in results if ok]
		# 		if not image_paths:
		# 			raise DropItem("Item contains no images")
		# 		item['image_paths'] = image_paths
		# 		return item
		######################################################################

		# Option 2: you can Drop the item if you think the data in this item is incorrect
		##########################################################################
		# from scrapy.exceptions import DropItem
		# raise DropItem("Missing price in %s" % item)

		# Option 3: you can dump the item to json file
		##############################################
		# import json
		# line = json.dumps(dict(item)) + "\n"
		# self.file.write(line)

	def close_spider(self, spider):
		print """######################\n"
		"# Now we're about to put the spider to sleep\n"
		"######################\n"""