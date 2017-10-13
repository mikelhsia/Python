import itertools
# itertools库可以生产各种迭代器，让迭代更加的高效。
# 一、 “无限”迭代器
# 无限序列在for迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，它不会事先把无限个元素生成出来。

# def count(start=0,step=1):
# 	# count(10) --> 10, 11, 12, 13, ...
# 	# count(5, 0,5) --> 5, 5.5, 6.0, 6.5
# 	n = start
# 	while True:
# 		yield n
# 		n += step

def cycle(iterable):
	pass

infinite_iter = itertools.count(start=0, step=1)

for x in infinite_iter:
	print(x)