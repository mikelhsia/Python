#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# TODO: Put the raw_input here instead of inside the spider
execute(["scrapy", "crawl", "fzdm"])
