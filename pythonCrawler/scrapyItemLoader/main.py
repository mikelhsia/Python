#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Put the raw_input here instead of inside the spider
manga      = raw_input("食戟之靈 - 58\t七原罪 - 56\t辛巴达 - 119\n"
                           "猎人 - 10\t东京RE - 117\n"
                           "进击 - 39\t英雄学院 - 131"
                           "\nInput Manga code: ")
targetChap = raw_input("Input start downloading chapter: ")
numChap    = raw_input("How many chapters you want to download: (-2 meaning download 2 chap before X) ")

exec_str = "scrapy crawl sil_spider -a manga=%s -a targetChap=%s -a numChap=%s" % (manga, targetChap, numChap)

execute(exec_str.split())
