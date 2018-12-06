# Using Submit 异步调用 2
# 异步调用: 提交/调用一个任务，不在原地等着，直接执行下一行代码

from concurrent.futures import ProcessPoolExecutor
import time, random, os


def piao(name, n):
	print(f"{name} is piaoing {os.getpid()}")
	time.sleep(1)
	return n ** 2


if __name__ == '__main__':
	p = ProcessPoolExecutor(2)
	objs = []
	start = time.time()

	for i in range(5):
		# 异步调用
		obj = p.submit(piao, f'safly {i}', i)
		print('obj appended {}'.format(i))
		objs.append(obj)

	for obj in objs:
		print(obj.result())

	p.shutdown(wait=True)
	print('主', os.getpid())

	end = time.time()
	print(end - start)