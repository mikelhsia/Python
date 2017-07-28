#!/usr/bin/python
# -*- coding: UTF-8 -*-


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
def printTime():
	return "当前时间为: %s" % (time.strftime("%Y-%m-%d" ,time.localtime(time.time())))
print printTime()

# raw_input([prompt]) 函数从标准输入读取一个行，并返回一个字符串（去掉结尾的换行符）：
# string = raw_input("请问你叫什么名字？ ")
# print "原来你是 %s 阿！" % string
# del string

# input([prompt]) 函数和 raw_input([prompt]) 函数基本类似，但是 input 可以接收一个Python表达式作为输入，并将运算结果返回。
# 请输入：[x*5 for x in range(2,10,2)]
# 你输入的内容是:  [10, 20, 30, 40]
# string = input("请输入列表组")
# print string

fo = open('/Users/tsuyuhsia/Desktop/Practice/ajax_info.txt', "r")
print "文件名: ", fo.name
print "是否已关闭 : ", fo.closed
print "访问模式 : ", fo.mode
print "末尾是否强制加空格 : ", fo.softspace  # 如果用print输出后，必须跟一个空格符，则返回false。否则返回true。

fi = open('/Users/tsuyuhsia/Desktop/Practice/ajax_info.txt2', "w+")
# fi.write(fo.read(20))
fi.write(fo.read())

position = fo.tell()
print "当前文件位置 : ", position
position = fo.seek(0, 0)
fi.write(fo.read(21))

fo.close()
print "是否已关闭 : ", fo.closed

## Exception 异常处理 ##
try:
	fh = open("testfile", "w")
	# fh = open("testfile", "r")
	try:
		fh.write("这是一个测试文件，用于测试异常!!")
	finally:
		print "关闭文件"
		fh.close()
except IOError, e: # 截取一个或是多个异常
	print "[Error]: 没有找到文件或读取文件失败"
	# print e
	# print "-------"
except:
	# Capture all errors
	print "[Error]: Unknown error occures"
else:
	print "[Else]: No error occurs"
finally:
	print "[Finally]: Try blocks end"

import os
os.remove("testfile")


# 定义函数
def temp_convert(var):
    try:
        return int(var)
    except ValueError, Argument:   # 一个异常可以带上参数，可作为输出的异常信息参数。
        print "参数没有包含数字\n[%s]" % Argument

temp_convert("abc"); # 调用函数

# 定义函数
print "------"
def mye(level):
    if level < 1:
        raise Exception("Invalid level! Err...", level)
        # 触发异常后，后面的代码就不会再执行

try:
    # mye(0)                # 触发异常
    mye(2)                # 触发异常
except "Invalid level! Err..":
    print 1
else:
    print 2
print "------"


'''
* 用户自定义异常
通过创建一个新的异常类，程序可以命名它们自己的异常。异常应该是典型的继承自Exception类，通过直接或间接的方式。
以下为与RuntimeError相关的实例,实例中创建了一个类，基类为RuntimeError，用于在异常触发时输出更多的信息。
在try语句块中，用户自定义的异常后执行except块语句，变量 e 是用于创建Networkerror类的实例
'''
class myPythonError(RuntimeError):
	def __init__ (self, arg):
		self.args = arg

try:
	raise myPythonError('Nothing')
except myPythonError, e:
	print "Customize Error"
	print e.args
else:
	print "Nothing happened"


# 文档重新命名
# os.rename('/Users/tsuyuhsia/Desktop/Practice/ajax_info.txt2', '/Users/tsuyuhsia/Desktop/Practice/ajax_info.txt3')
# os.remove()
# os.mkdir()
# os.rmdir()
# os.chdir()
# os.getcwd()

# A newer way to format strings is the format method.
# This method is the preferred way
print "{} is a {}".format("This", "placeholder")
print "{0} can be {1}".format("strings", "formatted")
# You can use keywords if you don't want to count.
print "{name} wants to eat {food}".format(name="Bob", food="lasagna")

