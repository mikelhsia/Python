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
		printTime(self.name, self.counter, 5)
		print "Ending this thread: ", self.name

def printTime(threadName, threadDelay, threadCounter):
	while threadCounter:
		if (exitFlag):
			threading.Thread.exit()
		time.sleep(threadDelay)
		print "%s: %s" % (threadName, time.ctime(time.time()))
		threadCounter -= 1

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
 
# 开启线程
thread1.start()
thread2.start()

print "\nExiting Main Thread\n"

