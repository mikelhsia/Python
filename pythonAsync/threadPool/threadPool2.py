from concurrent.futures import ProcessPoolExecutor
import time


def task(name):
	print('name', name)
	time.sleep(1)


if __name__ == '__main__':
	start = time.time()
	# Capacity of pool == 2
	ex = ProcessPoolExecutor(2)

	# Running 5 processes in these pools with 2 thread
	for i in range(5):
		ex.submit(task, "safly%d".format(i))

	# wait = False will end the main process first without waiting for the subprocess to end
	# ex.shutdown(wait=True)
	ex.shutdown(wait=False)

	print("main now")
	end = time.time()
	print(end - start)