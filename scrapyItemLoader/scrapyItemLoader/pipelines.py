# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib

class ScrapyitemloaderPipeline(object):

	def open_spider(self, spider):
		print """######################\n# Now we're about to awake the spider\n######################"""

	def process_item(self, item, spider):

		# Creating all the folder and file necessary
		dst = os.path.join(item['imgDst'], item['imgFileName'])

		try:
			os.mkdir(item['imgDst'])
		except:
			# self.log("[IOError]: folder is already exist!")
			pass

		urllib.urlretrieve(item['imgSrc'], dst)
		return item

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
		print """######################\n# Now we're about to put the spider to sleep\n ######################"""
