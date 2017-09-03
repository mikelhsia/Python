import time

####################################################################################
# Python thread
# thread.start_new_thread ( function, args[, kwargs] )
####################################################################################
from threading import Thread

class myThread (Thread):   #继承父类threading.Thread
	def __init__(self, name, counter):
		Thread.__init__(self)
		self.name     = name
		self.counter  = counter

	def run(self): #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
		print("Starting this thread: ", self.name)
		print_time(self.name, self.counter)
		print("Ending this thread: ", self.name)

def print_time(threadName, delay):
	count = 0
	while count < 5:
		time.sleep(delay)
		count += 1
		print("[%d] %s: %s" % (count, threadName, time.ctime(time.time())))

thread1 = myThread("Thread 1-1", 2)
thread2 = myThread("Thread 1-2", 4)

try:
	thread1.start()
	thread2.start()
except Exception as e:
	print("Error: unable to start thread")
	print(e)
else:
	pass

while True:
	pass


# 线程的结束一般依靠线程函数的自然结束；也可以在线程函数中调用thread.exit()，他抛出SystemExit exception，达到退出线程的目的。

# thread 模块提供的其他方法：
# - threading.currentThread(): 返回当前的线程变量。
# - threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
# - threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果

# hread类提供了以下方法
# - run(): 用以表示线程活动的方法。
# - start():启动线程活动。
# - join([time]): 等待至线程中止。这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
# - isAlive(): 返回线程是否活动的。
# - getName(): 返回线程名。
# - setName(): 设置线程名。
