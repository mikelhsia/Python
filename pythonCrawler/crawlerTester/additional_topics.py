#!/usr/local/bin/python
# -*- coding: utf-8 -*-


###################################################################################
# Run Scrapy as python script
###################################################################################
# from scrapy.cmdline import execute
# import sys
# import os
# Put the raw_input here instead of inside the spider
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# manga      = int(raw_input("食戟之靈 - 58\t七原罪 - 56\t辛巴达 - 119\n"
#                            "猎人 - 10\t东京RE - 117\n"
#                            "进击 - 39\t英雄学院 - 131"
#                            "\nInput Manga code: "))
# targetChap = int(raw_input("Input start downloading chapter: "))
# numChap    = int(raw_input("How many chapters you want to download: "))
# exec_str = "scrapy crawl sil_spider -a manga=%s -a targetChap=%s -a numChap=%s" % (manga, targetChap, numChap)
# execute(exec_str.split())
###################################################################################



###################################################################################
# Avoiding getting banned
###################################################################################
# Some websites implement certain measures to prevent bots from crawling them, with varying degrees of
# sophistication. Getting around those measures can be difficult and tricky, and may sometimes require
# special infrastructure. Please consider contacting commercial support if in doubt.
#
# Here are some tips to keep in mind when dealing with these kinds of sites:
# - rotate your user agent from a pool of well-known ones from browsers (google around to get a list of them)
# - disable cookies (see COOKIES_ENABLED) as some sites may use cookies to spot bot behaviour
# - use download delays (2 or higher). See DOWNLOAD_DELAY setting.
# - if possible, use "Google cache" to fetch pages, instead of hitting the sites directly
#   - http://www.googleguide.com/cached_pages.html
# - use a pool of rotating IPs. For example, the free Tor project or paid services like ProxyMesh. An open source alternative is scrapoxy, a super proxy that you can attach your own proxies to.
# - use a highly distributed downloader that circumvents bans internally, so you can just focus on parsing clean pages. One example of such downloaders is Crawlera
#
# If you are still unable to prevent your bot getting banned, consider contacting commercial support.
###################################################################################



###################################################################################
# Running multiple spiders in the same process - EX1
###################################################################################
# import scrapy
# from scrapy.crawler import CrawlerProcess
#
# class MySpider1(scrapy.Spider):
#     # Your first spider definition
#     ...
#
# class MySpider2(scrapy.Spider):
#     # Your second spider definition
#     ...
#
# process = CrawlerProcess()
# process.crawl(MySpider1)
# process.crawl(MySpider2)
# process.start() # the script will block here until all crawling jobs are finished
###################################################################################
# Running multiple spiders in the same process - EX2
###################################################################################
# import scrapy
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
#
# class MySpider1(scrapy.Spider):
#     # Your first spider definition
#     ...
#
# class MySpider2(scrapy.Spider):
#     # Your second spider definition
#     ...
#
# configure_logging()
# runner = CrawlerRunner()
# runner.crawl(MySpider1)
# runner.crawl(MySpider2)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
#
# reactor.run() # the script will block here until all crawling jobs are finished
###################################################################################
# Running multiple spiders in the same process - EX3
###################################################################################
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
#
# class MySpider1(scrapy.Spider):
#     # Your first spider definition
#     ...
#
# class MySpider2(scrapy.Spider):
#     # Your second spider definition
#     ...
#
# configure_logging()
# runner = CrawlerRunner()
#
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(MySpider1)
#     yield runner.crawl(MySpider2)
#     reactor.stop()
#
# crawl()
# reactor.run() # the script will block here until the last crawl call is finished
###################################################################################



###################################################################################
# Run Scrapy from a script
# https://doc.scrapy.org/en/latest/topics/practices.html
###################################################################################
# import scrapy
# from scrapy.crawler import CrawlerProcess
#
# class MySpider(scrapy.Spider):
#     # Your spider definition
#     ...
#
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(MySpider)
# process.start() # the script will block here until the crawling is finished
###################################################################################
