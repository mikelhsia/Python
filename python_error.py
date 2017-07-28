#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ZeroDivisionError
# NameError
# TypeError

while True:
	try:
		x = int(raw_input("Please enger a number:"))
		break
	except (ValueError, RuntimeError, TypeError, NameError):
		print "Oops! That was no valid number. Try again..."

print "#########################"
import sys

try:
	f = open('myfile.txt')
	s = f.readline()
	i = int(s.strip())
except IOError as e:
	print "I/O error({0}): {1}".format(e.errno, e.strerror)
except ValueError:
	print "Could not convert data to an integer"
except:
	print "Unexpected error: ", sys,exc_info()[0]
	# 如果你需要明确一个异常是否抛出，但不想处理它， raise 语句可以让你很简单的重新抛出该异常:
	raise
else:
	print "Else others..."
finally:
	# 不管有没有发生异常， finally子句 在程序离开 try 后都一定会被执行。
	# 当 try 语句中发生了未被 except 捕获的异常（或者它发生在 except 或 else 子句中），在 finally 子句执行完后它会被重新抛出。
	print "Finally..."



try:
	# raise 语句允许程序员强制抛出一个指定的异常。例如:
	raise Exception("spam", 'eggs')
except Exception as inst:
	print type(inst)
	print inst.args
	print inst

	x,y=inst.args
	print "x = ", x
	print "y = ", y

class MyError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

try: 
	raise MyError(2*2)
except MyError as e:
	print "My exception occurred, value: ", e.value

raise MyError('oops!')

# 在这个例子中，Exception 默认的 __init__() 被覆盖。新的方式简单的创建 value 属性。这就替换了原来创建 args 属性的方式。
# 异常类中可以定义任何其它类中可以定义的东西，但是通常为了保持简单，只在其中加入几个属性信息，以供异常处理句柄提取。
# 如果一个新创建的模块中需要抛出几种不同的错误时，一个通常的作法是为该模块定义一个异常基类，
# 然后针对不同的错误类型派生出对应的异常子类:
class Error(Exception):
	"""Base class for exceptions in this module."""
	pass

class InputError(Error):
	"""Exception raised for errors in the input.

	Attributes:
		expression -- input expression in which the error occurred
		message -- explanation of the error
	"""

	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

class TransitionError(Error):
	"""
	Raised when an operation attempts a state transition that's not allowed.

	Attributes:
		previous -- state at beginning of transition
		next -- attempted new state
		message -- explanation of why the specific transition is not allowed
	"""

	def __init__(self, previous, next, message):
		self.previous = previous
		self.next = next
		self.message = message


