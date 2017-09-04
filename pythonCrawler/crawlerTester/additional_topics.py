#!/usr/local/bin/python
# -*- coding: utf-8 -*-


###################################################################################
# Run Scrapy as python script
###################################################################################
# from scrapy.cmdline import execute
# import sys
# import os
# Put the input here instead of inside the spider
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# manga      = int(input("食戟之靈 - 58\t七原罪 - 56\t辛巴达 - 119\n"
#                            "猎人 - 10\t东京RE - 117\n"
#                            "进击 - 39\t英雄学院 - 131"
#                            "\nInput Manga code: "))
# targetChap = int(input("Input start downloading chapter: "))
# numChap    = int(input("How many chapters you want to download: "))
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

###################################################################################
# Debugging memory leaks with "prefs()" in telnet
###################################################################################
# telnet localhost 6023
#
# >>> prefs()
# Live References
#
# ExampleSpider                       1   oldest: 15s ago
# HtmlResponse                       10   oldest: 1s ago
# Selector                            2   oldest: 0s ago
# FormRequest                       878   oldest: 7s ago
#
# or
# >>> from scrapy.spiders import Spider
# >>> prefs(ignore=Spider)
###################################################################################
# Debugging memory leaks with "trackref"
###################################################################################
# - scrapy.utils.trackref module
# Here are the functions available in the trackref module.
#
# - class scrapy.utils.trackref.object_ref
# Inherit from this class (instead of object) if you want to track live instances with the trackref module.
#
# - scrapy.utils.trackref.print_live_refs(class_name, ignore=NoneType)
# Print a report of live references, grouped by class name.
#  Parameters:
#    ignore (class or classes tuple) – if given, all objects from the specified class (or tuple of classes) will be ignored.
#
# scrapy.utils.trackref.get_oldest(class_name)
# Return the oldest object alive with the given class name, or None if none is found.
# Use print_live_refs() first to get a list of all tracked live objects per class name.
#
# scrapy.utils.trackref.iter_all(class_name)
# Return an iterator over all objects alive with the given class name, or None if none is found.
# Use print_live_refs() first to get a list of all tracked live objects per class name.
###################################################################################
# Debugging memory leaks with Guppy
###################################################################################
# The telnet console also comes with a built-in shortcut (hpy) for accessing Guppy heap objects.
# Here’s an example to view all Python objects available in the heap using Guppy:
#
# >>> x = hpy.heap()
# >>> x.bytype
# Partition of a set of 297033 objects. Total size = 52587824 bytes.
#  Index  Count   %     Size   % Cumulative  % Type
#      0  22307   8 16423880  31  16423880  31 dict
#      1 122285  41 12441544  24  28865424  55 str
#      2  68346  23  5966696  11  34832120  66 tuple
#      3    227   0  5836528  11  40668648  77 unicode
#      4   2461   1  2222272   4  42890920  82 type
#      5  16870   6  2024400   4  44915320  85 function
#      6  13949   5  1673880   3  46589200  89 types.CodeType
#      7  13422   5  1653104   3  48242304  92 list
#      8   3735   1  1173680   2  49415984  94 _sre.SRE_Pattern
#      9   1209   0   456936   1  49872920  95 scrapy.http.headers.Headers
# <1676 more rows. Type e.g. '_.more' to view.>
###################################################################################
# You can see that most space is used by dicts. Then, if you want to see from which
# attribute those dicts are referenced, you could do:
#
# >>> x.bytype[0].byvia
# Partition of a set of 22307 objects. Total size = 16423880 bytes.
#  Index  Count   %     Size   % Cumulative  % Referred Via:
#      0  10982  49  9416336  57   9416336  57 '.__dict__'
#      1   1820   8  2681504  16  12097840  74 '.__dict__', '.func_globals'
#      2   3097  14  1122904   7  13220744  80
#      3    990   4   277200   2  13497944  82 "['cookies']"
#      4    987   4   276360   2  13774304  84 "['cache']"
#      5    985   4   275800   2  14050104  86 "['meta']"
#      6    897   4   251160   2  14301264  87 '[2]'
#      7      1   0   196888   1  14498152  88 "['moduleDict']", "['modules']"
#      8    672   3   188160   1  14686312  89 "['cb_kwargs']"
#      9     27   0   155016   1  14841328  90 '[1]'
# <333 more rows. Type e.g. '_.more' to view.>
###################################################################################
# Sometimes, you may notice that the memory usage of your Scrapy process will only increase,
# but never decrease. Unfortunately, this could happen even though neither Scrapy nor your project
# are leaking memory. This is due to a (not so well) known problem of Python, which may not return
# released memory to the operating system in some cases.
# - http://www.evanjones.ca/python-memory.html
# - http://www.evanjones.ca/python-memory-part2.html
# - http://www.evanjones.ca/python-memory-part3.html
###################################################################################



###################################################################################
# AutoThrottle extension
###################################################################################
# URL: https://doc.scrapy.org/en/latest/topics/autothrottle.html
#
# This is an extension for automatically throttling crawling speed based on load of
# both the Scrapy server and the website you are crawling.
#
# Design goals
# Be nicer to sites instead of using default download delay of zero
# automatically adjust scrapy to the optimum crawling speed, so the user doesn’t
# have to tune the download delays to find the optimum one. The user only needs to
# specify the maximum concurrent requests it allows, and the extension does the rest.
###################################################################################


###################################################################################
# Multiple cookie sessions per spider
# New in version 0.15.
###################################################################################
# There is support for keeping multiple cookie sessions per spider by using the cookiejar
# Request meta key. By default it uses a single cookie jar (session), but you can pass an identifier
# to use different ones.
#
# For example:
# for i, url in enumerate(urls):
#     yield scrapy.Request(url, meta={'cookiejar': i},
#         callback=self.parse_page)
#
# Keep in mind that the cookiejar meta key is not “sticky”. You need to keep passing it along on subsequent requests.
# For example:
# def parse_page(self, response):
#     # do some processing
#     return scrapy.Request("http://www.example.com/otherpage",
#         meta={'cookiejar': response.meta['cookiejar']},
#         callback=self.parse_other_page)
###################################################################################
