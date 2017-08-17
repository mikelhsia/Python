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
		print "######################\n# Now we're about to awake the spider\n######################"

	##############################################################################################################
	# process_request(request, spider)
	# This method is called for each request that goes through the download middleware.
	##############################################################################################################
	# process_request()
	# should either: return None, return a Response object, return a Request object, or raise IgnoreRequest.
	#
	# If it returns None, Scrapy will continue processing this request, executing all other middlewares until,
	# finally, the appropriate downloader handler is called the request performed( and its response downloaded).
	#
	# If it returns a Response object, Scrapy won’t bother calling any other process_request() or process_exception()
	# methods, or the appropriate download function; it’ll return that response.The process_response() methods of
	# installed middleware is always called on every response.
	#
	# If it returns a Request object, Scrapy will stop calling process_request methods and reschedule the returned
	# request.Once the newly returned request is performed, the appropriate middleware chain will be called on the
	# downloaded response.
	#
	# If it raises an IgnoreRequest exception, the process_exception() methods of installed downloader middleware will
	# be called.If none of them handle the exception, the errback function of the request(Request.errback) is called.
	# If no code handles the raised exception, it is ignored and not logged(unlike other exceptions).
	#
	# Parameters:
	# request(Request object) – the request being processed spider(Spider object) – the spider for which this request
	# is intended
	##############################################################################################################

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
		print "######################\n# Now we're about to put the spider to sleep\n######################"