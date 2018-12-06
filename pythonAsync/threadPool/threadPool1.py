from multiprocessing import Process
import time


def task(name):
	print("name", name)
	time.sleep(1)


if __name__ == '__main__':
	start = time.time()
	p1 = Process(target=task, args=('safly1',))
	p2 = Process(target=task, args=('safly2',))
	p3 = Process(target=task, args=('safly3',))

	p1.start()
	p2.start()
	p3.start()

	p1.join()
	p2.join()
	p3.join()

	print('Now main')

	end = time.time()
	print(end - start)