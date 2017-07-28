#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

class MyClass:
	"""A simple example class"""
	i = 12345
	__update = "update"   # private copy of original update() method

	def __init__(self):
		print "No no, __init__"

	def f(self):
		print "Hello World!"



print MyClass.i

try:
	MyClass.f()
except:
	print "Exception..."

x = MyClass()
x.f()

try:
	print x.__update
except:
	print "This is private"

# 数据属性 相当于 Smalltalk 中的“实例变量”或 C++ 中的“数据成员”。和局部变量一样，数据属性不需要声明，
x.counter = 1
while x.counter < 10:
	x.counter = x.counter * 2

print x.counter
del x.counter

# class DerivedClassName(BaseClassName):
# class DerivedClassName(modname.BaseClassName):
# BaseClassName.methodname(self, arguments):

# 多继承: 
#############################################
# 你能想到的搜索属性从父类继承的深度优先，左到右，而不是搜索两次在同一个类层次结构中，其中有一个重叠。
# 因此，如果在 DerivedClassName （示例中的派生类）中没有找到某个属性，就会搜索 Base1 ，然后（递归的）搜索其基类，
# 如果最终没有找到，就搜索 Base2 ，以此类推。
# class DerivedClassName(Base1, Base2, Base3):
#     <statement-1>
#     .
#     .
#     .
#     <statement-N>


# 有时类似于 Pascal 中“记录（record）”或C中“结构（struct）”的数据类型很有用，
# 它将一组已命名的数据项绑定在一起。一个空的类定义可以很好的实现这它:
class Employee:
	pass

john = Employee() # Create an empty employee record

# Fill the fields of the record
john.name = 'John Doe'
john.dept = 'computer lab'
john.salary = 1000

class B(Exception):
	pass

class C(B):
	pass

class D(C):
	pass

for cls in [B, C, D]:
	try:
		raise cls()
	except D:
		print "D"
	except C:
		print "C"
	except B:
		print "B"


# Iterator 迭代器
s = 'abcd'
it = iter(s)
print it
print next(it)
print it.next()
print it.next()
print it.next()
# print it.next()

class Reverse:
	"""Iterator for looping over a sequence backwards."""
	def __init__(self, data):
		self.data = data
		self.index = len(data)

	def __iter__(self):
		return self

	def __next__(self):
		if self.index == 0:
			raise StopInteration
		self.index = self.index - 1
		return self.data[self.data]

rev = Reverse('spam')
# print iter(rev)

# for char in rev:
# 	print char

# generator 生成器
# Generator 是创建迭代器的简单而强大的工具。它们写起来就像是正规的函数，需要返回数据的时候使用 yield 语句。
# 每次 next() 被调用时，生成器回复它脱离的位置（它记忆语句最后一次执行的位置和所有的数据值）。
def reverse(data):
	for index in range(len(data)-1,-1,-1):
		yield data[index]

for char in reverse("golfball"):
	print char


print sum(i*i for i in range(10))                 # sum of squares

xvec = [10, 20, 30]
yvec = [7, 5, 3]
print sum(x*y for x,y in zip(xvec, yvec))         # dot product

# from math import pi, sin
# sine_table = {x: sin(x*pi/180) for x in range(0, 91)}
# unique_words = set(word for line in page for word in line.split())
# valedictorian = max((student.gpa, student.name) for student in graduates)

data = 'golf'
print list(data[i] for i in range(len(data)-1, -1, -1))