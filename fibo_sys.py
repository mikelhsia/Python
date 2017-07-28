#!/usr/bin/python
# -*- coding: UTF-8 -*-

def fib(n):    # write Fibonacci series up to n
	a, b = 0, 1
	print "Inside Fib function", __name__
	while b < n:
		print b
		a, b = b, a+b


if __name__ == "__main__":
	import sys
# 可以python script.py <arguments> 的方式执行
# 如果模块被导入，不会执行这段代码: import fibo_sys的话
	fib(int(sys.argv[1]))

# from package import item
# 需要注意的是使用 from package import item 方式导入包时，这个子项（item）既可以是包中的一个子模块（或一个子包），
# 也可以是包中定义的其它命名，像函数、类或变量。import 语句首先核对是否包中有这个子项，如果没有，它假定这是一个模块，
# 并尝试加载它。如果没有找到它，会引发一个 ImportError 异常。

# import item.subitem.subsubitem
# 相反，使用类似 import item.subitem.subsubitem 这样的语法时，这些子项必须是包，最后的子项可以是包或模块，
# 但不能是前面子项中定义的类、函数或变量。

# 如果包中的 __init__.py 代码定义了一个名为 __all__ 的列表，就会按照列表中给出的模块名进行导入。
# 新版本的包发布时作者可以任意更新这个列表。如果包作者不想 import * 的时候导入他们的包中所有模块，那么也可能会决定不支持它（import *）

##############################
# str.rjust() 方法的演示，它把字符串输出到一列，并通过向左侧填充空格来使其右对齐。类似的方法还有 str.ljust() 和 str.center()。
# 这些函数只是输出新的字符串，并不改变什么。如果输出的字符串太长，它们也不会截断它，而是原样输出，这会使你的输出格式变得混乱，
# 不过总强过另一种选择（截断字符串），因为那样会产生错误的输出值。（如果你确实需要截断它，可以使用切割操作，
# 例如： x.ljust(n)[:n] 。）

# str.zfill() 它用于向数值的字符串表达左侧填充 0。该函数可以正确理解正负号:
for x in range(1,11):
	print repr(x).rjust(2), repr(x*x).rjust(3), repr(x*x*x).rjust(4)
for x in range(1,11):
	print '{0:2d} {1:3d} {2:4d}'.format(x,x*x,x*x*x)
print '12'.zfill(5)
print 'We are the {} who say "{}!"'.format('knights', 'Ni')
print 'This {food} is {adjective}.'.format(food='spam', adjective='absolutely horrible')

