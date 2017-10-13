#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function


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
#     python -c "import csv,json;print(json.dumps(list(csv.reader(open('csv_file.csv'))))")
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


##############################################
# 23. 协程
##############################################
# Python中的协程和生成器很相似但又稍有不同。主要区别在于：
# - 生成器是数据的生产者
# - 协程则是数据的消费者
# 这样做不仅快而且不会给内存带来压力，因为我们所需要的值都是动态生成的而不是将他们存储在一个列表中。
def fib():
	a, b = 0, 1
	while True and a <1000 :
		yield a
		a, b = b, a + b


for i in fib():
	print(i)

print_breakline()

def grep(pattern):
	print("Searching for", pattern)
	while True:
		line = (yield)
		# 发送的值会被yield接收。我们为什么要运行next()方法呢？
		# 这样做正是为了启动一个协程。就像协程中包含的生成器并不是立刻执行，
		# 而是通过next()方法来响应send()方法。因此，你必须通过next()方法来执行yield表达式。
		if pattern in line:
			print(line)

# 我们为什么要运行next()方法呢？这样做正是为了启动一个协程。
# 就像协程中包含的生成器并不是立刻执行，而是通过next()方法来响应send()方法。
# 因此，你必须通过next()方法来执行yield表达式。
search = grep('coroutine')
next(search)
#output: Searching for coroutine

search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutine instead!")
#output: I love coroutine instead!

# 我们可以通过调用close()方法来关闭一个协程。
search.close()


##############################################
# 函数缓存 (Function caching)
##############################################
# 函数缓存允许我们将一个函数对于给定参数的返回值缓存起来。
# 当一个I/O密集的函数被频繁使用相同的参数调用的时候，函数缓存可以节约时间。
# 在Python 3.2版本以前我们只有写一个自定义的实现。在Python 3.2以后版本，有个lru_cache的装饰器，
# 允许我们将一个函数的返回值快速地缓存或取消缓存。

# >= Python 3.2
#####
# 我们来实现一个斐波那契计算器，并使用lru_cache。
#
# from functools import lru_cache
#
# @lru_cache(maxsize=32)
# def fib(n):
#     if n < 2:
#         return n
#     return fib(n-1) + fib(n-2)
#
# >>> print([fib(n) for n in range(10)])
# # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
# 那个maxsize参数是告诉lru_cache，最多缓存最近多少个返回值。
# 我们也可以轻松地对返回值清空缓存，通过这样：
# fib.cache_clear()

# Python 2
#####
# 你可以创建任意种类的缓存机制，有若干种方式来达到相同的效果，这完全取决于你的需要。
# 这里是一个一般的缓存：
from functools import wraps

def memoize(function):
	memo = {}
	@wraps(function)
	def wrapper(*args):
		if args in memo:
			return memo[args]
		else:
			rv = function(*args)
			memo[args] = rv
			return rv
	return wrapper

@memoize
def fibonacci(n):
	if n < 2: return n
	return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(25)

print_breakline()
##############################################
# 上下文管理器(Context managers)
##############################################
# 上下文管理器允许你在有需要的时候，精确地分配和释放资源。
# 使用上下文管理器最广泛的案例就是with语句了
# 想象下你有两个需要结对执行的相关操作，然后还要在它们中间放置一段代码。
# 上下文管理器就是专门让你做这种事情的。举个例子：
# with open('some_file', 'w') as opened_file:
# 	opened_file.write('Hola!')
# 上下文管理器的一个常见用例，是资源的加锁和解锁，以及关闭已打开的文件（就像我已经展示给你看的）。
#####
# - 基于类的实现
# - 处理异常
# - 基于生成器的实现

# 1. 基于类的实现
#####
# 一个上下文管理器的类，最起码要定义__enter__和__exit__方法。

class File(object):
	def __init__(self, file_name, method):
		self.file_obj = open(file_name, method)

	def __enter__(self):
		return self.file_obj

	# def __exit__(self, type, value, traceback):
	def __exit__(self, exc_type, exc_val, exc_tb):
		print("Exception has been handled!")
		print("""Type: {} \nValue: {} \nTraceback: {}""".format(exc_type, exc_val, exc_tb))
		self.file_obj.close()
		return True # 返回了True,因此没有异常会被with语句抛出

# 通过定义__enter__和__exit__方法，我们可以在with语句里使用它
with File('demo.txt', 'w') as opened_file:
	opened_file.write("Hola!")

# 2. 处理异常
# 我们的__exit__函数接受三个参数。这些参数对于每个上下文管理器类中的__exit__方法都是必须的。我们来谈谈在底层都发生了什么。
#####
# 1. with语句先暂存了File类的__exit__方法
# 2. 然后它调用File类的__enter__方法
# 3. __enter__方法打开文件并返回给with语句
# 4. 打开的文件句柄被传递给opened_file参数
# 5. 我们使用.write()来写文件
# 6. with语句调用之前暂存的__exit__方法
# 7. __exit__方法关闭了文件

# 我们还没有谈到__exit__方法的这三个参数：type, value和traceback。
# 在第4步和第6步之间，如果发生异常，Python会将异常的type,value和traceback传递给__exit__方法。
# 它让__exit__方法来决定如何关闭文件以及是否需要其他步骤。

# 当异常发生时，with语句会采取哪些步骤:
# 1. 它把异常的type,value和traceback传递给__exit__方法
# 2. 它让__exit__方法来处理异常
# 3. 如果__exit__返回的是True，那么这个异常就被优雅地处理了。
# 4. 如果__exit__返回的是True以外的任何东西，那么这个异常将被with语句抛出。
with File('demo.txt', 'w') as opened_file:
	opened_file.undefined_function("Hola")

# 3. 基于生成器的实现
#####
# 我们还可以用装饰器(decorators)和生成器(generators)来实现上下文管理器。
# Python有个contextlib模块专门用于这个目的。我们可以使用一个生成器函数来实现一个上下文管理器，而不是使用一个类。
# 让我们看看一个基本的，没用的例子：

from contextlib import contextmanager

@contextmanager
def open_file(name):
	f = open(name, 'w')
	yield f
	f.close()

# 剖析下这个方法。
# 1. Python解释器遇到了yield关键字。因为这个缘故它创建了一个生成器而不是一个普通的函数。
# 2. 因为这个装饰器，contextmanager会被调用并传入函数名（open_file）作为参数。
# 3. contextmanager函数返回一个以GeneratorContextManager对象封装过的生成器。
# 4. 这个GeneratorContextManager被赋值给open_file函数，我们实际上是在调用GeneratorContextManager对象。

# 新生成的上下文管理器了，像这样：
# with open_file('some_file') as f:
# 	f.write('hola!')