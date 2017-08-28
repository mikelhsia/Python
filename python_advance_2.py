#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

def print_breakline():
	print("--------------------------------")

##############################################
# 各种推导式(comprehensions)
##############################################
# 推导式（又称解析式）是Python的一种独有特性，如果我被迫离开了它，我会非常想念。推导式是可以从一个数据序列构建另一个新的数据序列的结构体。 共有三种推导，在Python2和3中都有支持：
# - 列表(list)推导式
# - 字典(dict)推导式
# - 集合(set)推导式
# 我们将一一进行讨论。一旦你知道了使用列表推导式的诀窍，你就能轻易使用任意一种推导式了。
##############################################
# 字典推导式（dict comprehensions）
mcase = {'a': 10, 'b': 34, 'A': 7, 'Z': 3}

mcase_frequency = {
    k.lower(): mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0)
    for k in mcase.keys()
}

print(mcase)
print(mcase_frequency)
# mcase_frequency == {'a': 17, 'z': 3, 'b': 34}

mcase_fre = {v: k for k, v in mcase.items()}
print(mcase_fre)
# 快速对换一个字典的键和值

# 集合推导式（set comprehensions）
# 它们跟列表推导式也是类似的。 唯一的区别在于它们使用大括号{}。
squared = {x**2 for x in [1, 1, 2]}
print(squared)
# Output: {1, 4}

print_breakline()
##############################################
# 处理多个异常
# 我们可以使用三种方法来处理多个异常。
##############################################
# 第一种方法需要把所有可能发生的异常放到一个元组里
try:
	file = open('test.txt', 'rb')
except (IOError, EOFError) as e:
	print("An error occurred. {}".format(e.args[-1]))
	print(e)

# 另外一种方式是对每个单独的异常在单独的except语句块中处理。我们想要多少个except语句块都可以
try:
	file = open('test.txt', 'rb')
except EOFError as e:
	print("An EOF error occurred.")
	pass
	# raise e
except IOError as e:
	print("An error occurred.")
	pass
	# raise e

# 最后一种方式会捕获所有异常：
try:
	file = open('test.txt', 'rb')
except Exception:
	# 打印一些异常日志，如果你想要的话
	print("Capture all exceptions")
	pass
	# raise

# finally从句: 包裹到finally从句中的代码不管异常是否触发都将会被执行。这可以被用来在脚本执行之后做清理工作
try:
	file = open('test.txt', 'rb')
except IOError as e:
	print('An IOError occurred. {}'.format(e.args[-1]))
finally:
	print("This would be printed whether or not an exception occurred!")
# Output: An IOError occurred. No such file or directory
# This would be printed whether or not an exception occurred!

try:
	print('I am sure no exception is going to occur!')
except Exception:
	print('exception')
else:
	# 这里的代码只会在try语句里没有触发异常时运行,
	# 但是这里的异常将 *不会* 被捕获
	# !else从句只会在没有异常的情况下执行，而且它会在finally语句之前执行。
	print('This would only run if no exception occurs. And an error here '
			'would NOT be caught.')
finally:
	print('This would be printed in every case.')
# Output: I am sure no exception is going to occur!
# This would only run if no exception occurs.
# This would be printed in every case.

print_breakline()
##############################################
# lambda表达式
##############################################
# lambda表达式是一行函数。
# 它们在其他语言中也被称为匿名函数。如果你不想在程序中对一个函数使用两次，你也许会想用lambda表达式，它们和普通的函数完全一样。
# 原型: lambda 参数:操作(参数)
# 例子
add = lambda x, y: x + y

print(add(3, 5))
# Output: 8

a = [(1, 2), (4, 1), (9, 10), (13, -3)]
a.sort(key=lambda x: x[1])
print(a)
# Output: [(13, -3), (4, 1), (1, 2), (9, 10)]

# Example 2: 列表并行排序
# data = zip(list1, list2)
# data.sort()
# list1, list2 = map(lambda t: list(t), zip(*data))


# 如果你想快速漂亮的从文件打印出json数据，那么你可以这么做：
#     cat file.json | python -m json.tool
# 脚本性能分析 这可能在定位你的脚本中的性能瓶颈时，会非常奏效：
#     python -m cProfile my_script.py
# 备注：cProfile是一个比profile更快的实现，因为它是用c写的
# CSV转换为json，在命令行执行这条指令
#     python -c "import csv,json;print json.dumps(list(csv.reader(open('csv_file.csv'))))"
# 列表辗平: 您可以通过使用itertools包中的itertools.chain.from_iterable轻松快速的辗平一个列表。下面是一个简单的例子：
#     a_list = [[1, 2], [3, 4], [5, 6]]
#     print(list(itertools.chain.from_iterable(a_list)))
#     # Output: [1, 2, 3, 4, 5, 6]
#
#     # or
#     print(list(itertools.chain(*a_list)))
#     # Output: [1, 2, 3, 4, 5, 6]
# 一行式的构造器:避免类初始化时大量重复的赋值语句
#     class A(object):
#         def __init__(self, a, b, c, d, e, f):
#             self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})

##############################################
# else从句
##############################################
# for循环还有一个else从句，我们大多数人并不熟悉。这个else从句会在循环正常结束时执行。
# 这意味着，循环没有遇到任何break. 一旦你掌握了何时何地使用它，它真的会非常有用。我自己对它真是相见恨晚。

# 1.
##############################################
# for item in container:
#     if search_something(item):
#         # Found it!
#         process(item)
#         break
# else:
#     # Didn't find anything..
#     not_found_in_container()

# 2.
##############################################
# for n in range(2, 10):
#     for x in range(2, n):
#         if n % x == 0:
#             print(n, 'equals', x, '*', n/x)
#             break

# 1 + 2
# 它会找出2到10之间的数字的因子。现在是趣味环节了。我们可以加上一个附加的else语句块，来抓住质数，并且告诉我们：
##############################################
for n in range(2, 10):
	for x in range(2, n):
		if n % x == 0:
			print( n, 'equals', x, '*', n/x)
			break
	else:
		# loop fell through without finding a factor
		print(n, 'is a prime number')


##############################################
# 使用C扩展
##############################################
# CPython还为开发者实现了一个有趣的特性，使用Python可以轻松调用C代码
# 首先，我们要明确为什么要在Python中调用C？
# 常见原因如下：
#       - 你要提升代码的运行速度，而且你知道C要比Python快50倍以上
#       - C语言中有很多传统类库，而且有些正是你想要的，但你又不想用Python去重写它们
#       - 想对从内存到文件接口这样的底层资源进行访问
#       - 不需要理由，就是想这样做
# 3 extensions:
#   - CTypes
#   - SWIG
#   - Python/C API
#####


##############################################
# open函数
##############################################
# f = open('photo.jpg', 'r+')
# jpgdata = f.read()
# f.close()


# New
#####
# with open('photo.jpg', 'r+') as f:
# 	jpgdata = f.read()

##############################################
# 目标Python2 + 3
##############################################
# 兼顾 Python 2 与 Python 3的兼容性