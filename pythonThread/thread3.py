#!/usr/bin/python
# -*- coding: UTF-8 -*-

####################################################################################
# Python thread
# thread.start_new_thread ( function, args[, kwargs] )
####################################################################################
import threading
import time

exitFlag = False

class myThread (threading.Thread):   #继承父类threading.Thread
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name     = name
		self.counter  = counter

	def run(self): #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
		print "Starting this thread: ", self.name
		# 获得锁，成功获得锁定后返回True
		# 可选的timeout参数不填时将一直阻塞直到获得锁定
		# 否则超时后将返回False
		threadLock.acquire()
		printTime(self.name, self.counter, 5)
		threadLock.release()
		print "Ending this thread: ", self.name

def printTime(threadName, threadDelay, threadCounter):
	while threadCounter:
		if (exitFlag):
			threading.Thread.exit()
		time.sleep(threadDelay)
		print "%s: %s" % (threadName, time.ctime(time.time()))
		threadCounter -= 1

threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
 
# 开启线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()

print "\nExiting Main Thread\n"