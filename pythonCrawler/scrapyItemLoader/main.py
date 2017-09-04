#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Put the input here instead of inside the spider
spider = input("风之动漫 - 1\tKuku动漫 - 2\t"
					"Which site you want to crawl: ")

if spider == '1':
	print("""http://comic.kukudm.com/\n*****************************""")
	manga = input("食戟之靈 - 58\t七原罪 - 56\t辛巴达 - 119\n"
						"猎人 - 10\t东京RE - 117\n"
						"进击的巨人 - 39\t英雄学院 - 131\n"
						"Input Manga code: ")
	targetChap = input("Input start downloading chapter: ")
	numChap = input("How many chapters you want to download: (-2 meaning download 2 chap before X) ")
	exec_str = "scrapy crawl sil_spider -a manga=%s -a targetChap=%s -a numChap=%s" % (manga, targetChap, numChap)
else:
	print("""http://manhua.fzdm.com\n*****************************""")
	manga = input("食戟之靈 - 1694\t七原罪 - 1733\t魔笛 - 982\n"
						"猎人 - 146\t东京RE - 1393\n"
						"进击的巨人 - 941\t英雄学院 - 2049\n"
						"Input Manga code: ")
	targetChap = input("Input start downloading chapter: ")
	numChap = input("How many chapters you want to download: (-2 meaning download 2 chap before X) ")
	exec_str = "scrapy crawl kuku_sil_spider -a manga=%s -a targetChap=%s -a numChap=%s" % (manga, targetChap, numChap)


execute(exec_str.split())
