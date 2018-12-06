# Using `Submit` 同步调用
# 同步调用：提交/调用一个任务，然后就在原地等着，等到该任务执行完毕拿到结果，再执行下一行代码


from concurrent.futures import ProcessPoolExecutor
import time, random, os


def piao(name, n):
	print(f"{name} is piaoing {os.getpid()}")
	time.sleep(1)
	return n ** 2


if __name__ == '__main__':
	p = ProcessPoolExecutor(2)
	start = time.time()

	for i in range(5):
		# 同步调用
		res = p.submit(piao, f'safly {i}', i).result()
		print(res)

	p.shutdown(wait=True)
	print('主', os.getpid())

	end = time.time()
	print(end - start)