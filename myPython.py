#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
 
# 以下划线开头的标识符是有特殊意义的。以单下划线开头 _foo 的代表不能直接访问的类属性，
# 需通过类提供的接口进行访问，不能用 from xxx import * 而导入；
# 以双下划线开头的 __foo 代表类的私有成员；以双下划线开头和结尾的 __foo__ 代表 Python 
# 里特殊方法专用的标识，如 __init__() 代表类的构造函数。

# 学习 Python 与其他语言最大的区别就是，Python 的代码块不使用大括号 {} 来控制类，函数以及其他逻辑判断。
# python 最具特色的就是用缩进来写模块。

if True:
	print "Answer"
	print "True"
else:
	print "Answer"
    # 没有严格缩进，在执行时会报错
	print "False"

print '---------'
print """3\n21,
而且还可以分行\n"""

"""
多行注释
多行注释
多行注释
多行注释
多行注释
多行注释
"""
import sys; x = 'runoob'; sys.stdout.write(x + '\n')

print '---------'
x="a"
y="b"
# 换行输出
print "x: ", x
print "y: ", y

print '---------'
# 不换行输出
print "x: ", x,
print "y: ", y

print '---------'
# Python字符串
str = 'Hello World!'
del x,y
 
print str           # 输出完整字符串
print str[0]        # 输出字符串中的第一个字符
print str[2:5]      # 输出字符串中第三个至第五个之间的字符串
print str[2:]       # 输出从第三个字符开始的字符串
print str * 2       # 输出字符串两次
print str + "TEST"  # 输出连接的字符串

print '---------'
# Python 列表
list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
tinylist = [123, 'john']
 
print list               # 输出完整列表
print list[0]            # 输出列表的第一个元素
print list[1:3]          # 输出第二个至第三个的元素 
print list[2:]           # 输出从第三个开始至列表末尾的所有元素
print tinylist * 2       # 输出列表两次
print list + tinylist    # 打印组合的列表

del tinylist

print '---------'
# Python 元组
# 元组是另一个数据类型，类似于List（列表）。
# 元组用"()"标识。内部元素用逗号隔开。但是元组不能二次赋值，相当于只读列表。
tuple = ( 'runoob', 786 , 2.23, 'john', 70.2 )	# tuple 将序列 s 转换为一个元组
tinytuple = (123, 'john')
 
print tuple               # 输出完整元组
print tuple[0]            # 输出元组的第一个元素
print tuple[1:3]          # 输出第二个至第三个的元素 
print tuple[2:]           # 输出从第三个开始至列表末尾的所有元素
print tinytuple * 2       # 输出元组两次
print tuple + tinytuple   # 打印组合的元组

del tinytuple
# tuple[0] = 123			# 元组不能二次赋值，相当于只读列表

print '---------'
# Python 字典
# 字典(dictionary)是除列表以外python之中最灵活的内置数据结构类型。列表是有序的对象结合，字典是无序的对象集合。
# 两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取。
# 字典用"{ }"标识。字典由索引(key)和它对应的值value组成。
dict = {}
dict['one'] = "This is one"
dict[2] = "This is two"
 
tinydict = {'name': 'john','code':6734, 'dept': 'sales'}
 
print dict['one']          # 输出键为'one' 的值
print dict[2]              # 输出键为 2 的值
print tinydict             # 输出完整的字典
print tinydict.keys()      # 输出所有键
print tinydict.values()    # 输出所有值
del tinydict['code']
print tinydict.values()    # 输出所有值

del tinydict

flag = 0
if (flag<<1):
	print flag
else:
	print flag
del flag

var = 99 
if ( var  == 100 ) : print "变量 var 的值为100"
del var

# Python has special "while ... else ..." condition 
count = 0
while count < 5:
	print count, " is  less than 5"
	count = count + 1
else:
	print count, " is not less than 5"
del count

var1 = var2 = 'Hello World!'

var2 = var1[:6] + 'Runnob!'
print "更新字符串 :- ", var1[:6] + 'Runoob!'
print "var1 字符串:- ", var1
print "var2 字符串:- ", var2
del var1, var2

print "My name is %s and weight is %d kg!" % ('Zara', 21) 

# Unicode
print u'Hello\u0020 \u0028 \u0029 World!'
print u"\u7f8e\u8f1d\u8857\uff0c\u7f8e\u7530\u90a8"
print u"\u571f\u74dc\u7063\u7f8e\u666f\u885755\u865f\u5b89\u5eb7\u5927\u5ec8\u4e00\u6a13b\u5ba4"
print u"\u4e5d\u9f8d\u4f55\u6587\u7530\u5fe0\u5b5d\u885760\u865f\u611b\u6c11\u90a8\u980c\u6c11\u6a1317\u6a131719\u5ba4 Hong Kong"

import time
# You can shorten module names
# import time as m

i = 5
def printTime(xx = i):	# 默认值在函数 定义 作用域被解析, so i=5
	return "当前时间为: %s" % (time.strftime("%Y-%m-%d" ,time.localtime(time.time())))
print printTime()

i=6

dictionary={}
dictionary['1'] = 'one'
print dictionary['1']

x='2'
dictionary[x] = 'two'
print dictionary[x]


# 重要警告: 默认值只被赋值一次。这使得当默认值是可变对象时会有所不同，
# 比如列表、字典或者大多数类的实例。例如，
# 下面的函数在后续调用过程中会累积（前面）传给它的参数:
def f(a, L=[]):
    L.append(a)
    return L

print f(1)
print f(2)
print f(3)


squares = [x**2 for x in range(10)]


print [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
# 等同于
# >>> combs = []
# >>> for x in [1,2,3]:
# ...     for y in [3,1,4]:
# ...         if x != y:
# ...             combs.append((x, y))
# ...
# >>> combs


matrix=[[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
print [[row[i] for row in matrix] for i in range(3)]

t = 12345,54321,"abcde"
print t

x, y, z = t
print x, ', ', y, ', ', z

# 直接创造字典
# a = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])

# 更简单创造字典
print {x: x**2 for x in (2, 4, 6)}

# 更快
# print dict(sape=4139, guido=4127, jack=4098)


questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q,a in zip(questions,answers):
	print 'What is your {0}?  It is {1}.'.format(q, a)