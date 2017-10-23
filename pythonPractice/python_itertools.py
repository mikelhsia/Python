import itertools
# itertools库可以生产各种迭代器，让迭代更加的高效。
# 一、 “无限”迭代器
# 无限序列在for迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，它不会事先把无限个元素生成出来。

###################################################################
# def count(start=0,step=1):
# 	# count(10) --> 10, 11, 12, 13, ...
# 	# count(5, 0,5) --> 5, 5.5, 6.0, 6.5
# 	n = start
# 	while True:
# 		yield n
# 		n += step

# infinite_iter = itertools.count(start=0, step=1)
#
# for x in infinite_iter:
# 	print(x)

###################################################################
def cycle(iterable):
	# cycle()会把传入的一个序列无限重复下去
	# cycle('ABCD') --> A B C D A B C D A B C D ...
	saved = []
	# 迭代最初的元素
	for element in iterable:
		yield element
		saved.append(element)
		# 执行完该for回圈后，为了继续循环往下，执行下面的while语句
	while saved:
		for element in saved:
			yield element


abc = itertools.cycle('ABC')
for x in abc:
	print(x)


###################################################################
def repeat(object, times=None):
	# 负责把一个元素element无限重复下去，如果提供第二个参数，个可以限定重复次数
	# repeat(10,3) --> 10, 10, 10
	if times is None:
		while True:
			yield object
	else:
		for i in range(times):
			yield object


repetition = itertools.repeat('a', 10)
for n in repetition:
	print(n)


###################################################################
# 无限序列虽然可以无限迭代下去，但是通常我们会通过takewhile()等函数根据条件判断来截取出一个有限的序列
# itertools.takewhile(predicate, iterable) 返回满足predicate条件的迭代器中的元素。


###################################################################
# 操作价值极高的几个函数

# 2.1 Chain()
# chain() 將括號內的所有可迭代對象，共同順序輸出至一個迭代對象，相當於是把多個可迭代對象拼接起來
def chain (*iterables):
	# chain('ABC', 'DEF') --> A B C D E F
	for it in iterables:
		for element in it:
			yield element

for x in itertools.chain([['a', 'b'], ['c', 'd']], 'DEF'):
	print(x)

# Results:
# ['a', 'b']
# ['c', 'd']
# D
# E
# F

# 2.2 groupby()
# groupby() 把迭代器中相鄰的重複元素挑出來放在一起，分成不同的部分
groups = itertools.groupby('AAAABBBCCDDDDDDDDDAABABV')
for key,group in groups:
	print(key, list(group))

for key, group in itertools.groupby('AaaBBbcCAAa', key=lambda c: c.lower()):
	print(key, list(group))

# 2.3 accumulate(iterable, func=operator.add)
# 默认func为累加，具体可看下面运行找规律。
import operator
def accumulate(iterable, func=operator.add):
	#'Return running totals'
	# accumulate([1,2,3,4,5]) --> 1 3 6 10 15
	# accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
	it = iter(iterable)
	try:
		total = next(it)
	except StopIteration:
		#迭代对象迭代完退出该函数
		return

	yield total #yield的第一个和

	for element in it:
		#yield出total后，继续作为下一次迭代的传入的值
		total = func(total, element)
		yield total

for x in itertools.accumulate([1,2,3,4,5]):
	# 1, 3, 6, 10, 15
	print(x)

# 2.4 chain.from_iterable()
# 智能传入一个可迭代对象作为参数，并将最多两层嵌套关系摧毁。
for x in itertools.chain.from_iterable([['A','B'],'C']):
	#将[['A','B'],'C']所有元素迭代出来
	print(x) # A, B, C


# 2.5 compress(data,selector)
# data与selector均为可迭代对象，且长度相同。通过selector参数来挑选data中的数据。
# selector参数为0或非0。
#       如果为0,则不返回data中对应的值;
#       如果为非0，返回data中对应的值。

for x in itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1]):
	print(x)    # A, C, E, F

for x in itertools.compress('ABCDEF', [-1, 0, 3, 0, 1, 1]):
	print(x)    # A, C, E, F


# 2.6 dropwhile(pred, iterable)
# 返回剔除iterable中满足predicate条件的元素后序列。

#剔除掉[1,4,6,4,1]中小于5的元素
for x in itertools.dropwhile(lambda x: x<5, [1,4,6,4,1]):
	print(x)


# 2.7 filterfalse()
# filterfalse(predicate, iterable)
# 保留iterable中满足predicate条件的元素。

#保留[0,9)中能被2整除的数
for x in itertools.filterfalse(lambda x: x%2, range(10)):
	print(x)