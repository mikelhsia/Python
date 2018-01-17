import gevent
from pyquery import PyQuery as pq
import requests
import time
import gevent.monkey

# 因为requests库在任何时候只允许有一个访问结束完全结束后，才能进行下一次访问。无法通过正规途径拓展成异步，因此这里使用了monkey补丁
gevent.monkey.patch_all()


"""
url构建只需要传入word即可:
url = "http://dict.youdao.com/w/eng/{}/".format(word)
"""

def fetch_word_info(word):
	url = 'http://dict.youdao.com/w/eng/{}/'.format(word)

	# resp = requests.get(url, headers=headers)
	resp = requests.get(url)
	doc = pq(resp.text)

	pros = ''
	for pro in doc.items('.baav .pronounce'):
		pros += pro.text()


	description = ''
	for li in doc.items('#phrsListTab .trans-container ul li'):
		description += li.text()

	return {'word': word, '音标': pros, '注释': description}

words = ['good','bad','cool',
		'head','up','down',
		'right','left','east']


def synchronous():
	start = time.time()
	print('同步开始了')

	for word in words:
		print(fetch_word_info(word))

	end = time.time()
	print("同步运行时间: %s 秒" % str(end - start))

def asynchronous():
	start = time.time()
	print("异步开始了")

	events = [gevent.spawn(fetch_word_info, word) for word in words]
	wordinfos = gevent.joinall(events)

	for wordinfo in wordinfos:
		# 获取到数据get方法
		print(wordinfo.get())

	end = time.time()
	print("异步运行时间: %s 秒" % str(end - start))


# 执行同步
synchronous()

# 执行异步
asynchronous()