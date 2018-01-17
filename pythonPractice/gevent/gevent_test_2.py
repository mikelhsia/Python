import gevent
import random

"""
同步案例中所有的任务都是按照顺序执行，这导致主程序是阻塞式的（阻塞会暂停主程序的执行）。

gevent.spawn会对传入的任务（子任务集合）进行进行调度，gevent.joinall方法会阻塞当前程序，除非所有的greenlet都执行完毕，程序才会结束。
"""

def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(random.randint(0, 2) * 0.001)
    print("Task %s done" % pid)


# 同步(结果更像串行)
def synchronous():
    for i in range(1, 10):
        task(i)


# 异步(结果更像乱步)
def asynchronous():
    threads = [gevent.spawn(task, i) for i in range(10)]
    gevent.joinall(threads)

print('Synchronous同步:')
synchronous()

print('Asynchronous异步:')
asynchronous()
