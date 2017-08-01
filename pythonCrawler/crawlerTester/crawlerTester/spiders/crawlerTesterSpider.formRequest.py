# -*- coding: utf-8 -*-
import scrapy

class CrawlertesterspiderSpider(scrapy.Spider):
	name = 'crawlerTesterSpider'
	allowed_domains = ['https://meitaichina.alpha.tmogroup.asia']
	start_urls = ['https://meitaichina.alpha.tmogroup.asia/index.php/customer/account/login/']

	# rules = (Rule(LinkExtractor(allow=r'*'), callback='parse_item', follow=True), )

	def parse(self, response):
		# self.logger.debug("First time in the url", response.url)
		# TODO: Add User-agent...
		# FIXME: User-agent is taken cared in the middleware level already
		print "First time in the url: ", response.url
		# When working with forms that are filled and / or submitted using javascript, the default
		# from_response() behaviour may not be the most appropriate.To disable this behaviour
		# you can set the dont_click argument to True
		return scrapy.FormRequest.from_response(
			response,
			formdata={'username': '13817405123', 'password': '123123q'},
			callback=self.after_login,
			dont_filter=True
		)

	def after_login(self, response):
		# check login succeed before going on
		print "Start parsing login"
		if "authentication failed" in response.body:
			# self.logger.error("Login failed")
			print "Login failed"
			return
		else:
			print "Login successfully"
			print "body %s" % response.body
		# continue scraping with authenticated session...
