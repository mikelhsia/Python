from __future__ import division
import math
import sys
import time

import asyncio

def progressBar(cur, total):
	percent = '{:.2%}'.format(cur / total)
	sys.stdout.write('\r')
	sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)), percent))
	sys.stdout.flush()

progressBar(0.8, 100)
time.sleep(0.5)
progressBar(1, 100)
time.sleep(0.5)
progressBar(2.1, 100)
time.sleep(0.5)
progressBar(3.3, 100)
time.sleep(0.5)
progressBar(70.3, 100)

import seaborn as sns
sns.tsplot()
sns.pointplot()
