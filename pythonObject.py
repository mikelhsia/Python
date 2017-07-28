#!/usr/bin/python
# -*- coding: UTF-8 -*-

def printBreakLine():
	print "-------------------------"

class Employee:
	'所有员工的基类, self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。'
	empCount = 0
	species = "Human"
 
	def __init__(self, name, salary):
		self.name = name
		self.salary = salary
		Employee.empCount += 1

	def displayCount(self):
		print "Total Employee: %d" % Employee.empCount
 
	def displayEmployee(self):
		print "Name : ", self.name,  ", Salary: ", self.salary

	# self 不是 python 关键字，我们把他换成 runoob 也是可以正常执行的:
	def prt(self):
		print(self)
		print(self.__class__)

	# A class method is shared among all instances
	# They are called with the calling class as the first argument
	@classmethod
	def get_species(cls):
		return cls.species

	# A static method is called without a class or instance reference
	@staticmethod
	def grunt():
		return "*grunt*"

	# A property is just like a getter.
	# It turns the method age() into an read-only attribute
	# of the same name.
	@property
	def age(self):
		return self._age

	# This allows the property to be set
	@age.setter
	def age(self, age):
		self._age = age

	# This allows the property to be deleted
	@age.deleter
	def age(self):
		del self._age
 
emp1 = Employee("Michael", 1000)
emp1.prt() 
emp1.displayCount()
emp1.displayEmployee()
print "Total count of employees: ", emp1.empCount

# 可以添加，删除，修改类的属性，如下所示：
emp1.age = 7  # 添加一个 'age' 属性
print "emp1's age is: ", emp1.age
emp1.age = 8  # 修改 'age' 属性
print "Now emp1's age is: ", emp1.age
hasattr(emp1, 'age')    # 如果存在 'age' 属性返回 True。
getattr(emp1, 'age')    # 返回 'age' 属性的值
setattr(emp1, 'age', 8) # 添加属性 'age' 值为 8
delattr(emp1, 'age')    # 删除属性 'age'
# del emp1.age  # 删除 'age' 属性

# __dict__ : 类的属性（包含一个字典，由类的数据属性组成）
# __doc__ :类的文档字符串
# __name__: 类名
# __module__: 类定义所在的模块（类的全名是'__main__.className'，如果类位于一个导入模块mymod中，那么className.__module__ 等于 mymod）
# __bases__ : 类的所有父类构成元素（包含了一个由所有父类组成的元组）
print "Employee.__doc__:", Employee.__doc__
print "Employee.__name__:", Employee.__name__
print "Employee.__module__:", Employee.__module__
print "Employee.__bases__:", Employee.__bases__
print "Employee.__dict__:", Employee.__dict__

printBreakLine()

# python对象销毁(垃圾回收),  
#   这个对象的引用计数变为0 时， 它被垃圾回收。
#   但是回收不是"立即"的， 由解释器在适当的时机，将垃圾对象占用的内存空间回收
a = 40      # 创建对象  <40>
b = a       # 增加引用， <40> 的计数
c = [b]     # 增加引用.  <40> 的计数

del a       # 减少引用 <40> 的计数
b = 100     # 减少引用 <40> 的计数
c[0] = -1   # 减少引用 <40> 的计数

printBreakLine()

class Point:
	def __init__( self, x=0, y=0):
		self.x = x
		self.y = y
	def __del__(self):
		class_name = self.__class__.__name__
		print class_name, "销毁"
 
pt1 = Point()
pt2 = pt1
pt3 = pt1
print id(pt1), id(pt2), id(pt3) # 打印对象的id
del pt1
del pt2
del pt3

printBreakLine()

# 继承语法 class 派生类名（基类名）
# 在python中继承中的一些特点：
# 	1：在继承中基类的构造（__init__()方法）不会被自动调用，它需要在其派生类的构造中亲自专门调用。
# 	2：在调用基类的方法时，需要加上基类的类名前缀，且需要带上self参数变量。区别于在类中调用普通函数时并不需要带上self参数
# 	3：Python总是首先查找对应类型的方法，如果它不能在派生类中找到对应的方法，它才开始到基类中逐个查找。
#    （先在本类中查找调用的方法，找不到才去基类中找）。

class Parent:        # 定义父类
	parentAttr = 100
	def __init__(self):
		print "调用父类构造方法"
 
	def parentMethod(self):
		print '调用父类方法'

	def setAttr(self, attr):
		Parent.parentAttr = attr

	def getAttr(self):
		print "父类属性 :", Parent.parentAttr
 
class Child(Parent): # 定义子类
	def __init__(self):
		Parent.__init__(self) # 调用父类构造方法
		print "调用子类构造方法"

	def childMethod(self):
		print '调用子类方法 child method'
 
c = Child()          # 实例化子类, 同时调用父类及子类的建构方法
c.childMethod()      # 调用子类的方法
c.parentMethod()     # 调用父类方法
c.setAttr(200)       # 再次调用父类的方法
c.getAttr()          # 再次调用父类的方法

printBreakLine()

# 多类继承
#####################################
# class A:        # 定义类 A
# .....
# class B:         # 定义类 B
# .....
# class C(A, B):   # 继承类 A 和 B
# .....

# issubclass() - 布尔函数判断一个类是另一个类的子类或者子孙类，语法：issubclass(sub,sup)
# isinstance(obj, Class) 布尔函数如果obj是Class类的实例对象或者是一个Class子类的实例对象则返回true。


# 方法重写: 如果你的父类方法的功能不能满足你的需求，你可以在子类重写你父类的方法

class Parent1:        # 定义父类
	def myMethod(self):
		print '调用父类方法'
 
class Child1(Parent1): # 定义子类
	def myMethod(self):
		print '调用子类方法'
 
c = Child1()          # 子类实例
c.myMethod()         # 子类调用重写方法

printBreakLine()

# 运算符重载：
# 1	__init__ ( self [,args...] ) 构造函数
# 		简单的调用方法: obj = className(args)
# 2	__del__( self ) 析构方法, 删除一个对象
# 		简单的调用方法 : dell obj
# 3	__repr__( self ) 转化为供解释器读取的形式
# 		简单的调用方法 : repr(obj)
# 4	__str__( self ) 用于将值转化为适于人阅读的形式
# 		简单的调用方法 : str(obj)
# 5	__cmp__ ( self, x ) 对象比较
# 		简单的调用方法 : cmp(obj, x)
class Vector:
	def __init__(self, a, b):
		self.a = a
		self.b = b
 
	def __str__(self):
		return 'Vector (%d, %d)' % (self.a, self.b)
 
	def __add__(self,other):
		return Vector(self.a + other.a, self.b + other.b)
 
v1 = Vector(2,10)
v2 = Vector(5,-2)
print v1
print v2
print v1 + v2

printBreakLine()

class JustCounter:
    __secretCount = 0  # 私有变量
    publicCount = 0    # 公开变量
 
    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print self.__secretCount
 
counter = JustCounter()
counter.count()
counter.count()
print counter.publicCount
# print counter.__secretCount  # 报错，实例不能访问私有变量

# Python不允许实例化的类访问私有数据，但你可以使用 object._className__attrName 访问属性，将如下代码替换以上代码的最后一行代码
print counter._JustCounter__secretCount 

# 单下划线、双下划线、头尾双下划线说明：
# __foo__: 定义的是特列方法，类似 __init__() 之类的。
# _foo: 以单下划线开头的表示的是 protected 类型的变量，即保护类型只能允许其本身与子类进行访问，不能用于 from module import *
# __foo: 双下划线的表示的是私有类型(private)的变量, 只能是允许这个类本身进行访问了。

printBreakLine()

# Regular expression: 
# re.match(pattern, string, flags=0)
# re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none。
import re
print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配


line = "Cats are smarter than dogs"
matchObj = re.match( r'(.*) are (.*?) (.*)', line, re.M|re.I)
 
if matchObj:
   print "matchObj.group()  : ", matchObj.group()
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2) # .*? 后面多个问号，代表非贪婪模式，只匹配符合条件的最少字符
   print "matchObj.group(3) : ", matchObj.group(3)
else:
   print "No match!!"

printBreakLine()
# re.match与re.search的区别
# re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配。
print(re.search('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.search('com', 'www.runoob.com').span())         # 不在起始位置匹配


line = "Cats are smarter than dogs"
searchObj = re.search( r'(.*) are (.*?) (.*)', line, re.M|re.I)
 
if searchObj:
   print "searchObj.group()  : ", searchObj.group()
   print "searchObj.group(1) : ", searchObj.group(1)
   print "searchObj.group(2) : ", searchObj.group(2) # .*? 后面多个问号，代表非贪婪模式，只匹配符合条件的最少字符
   print "searchObj.group(3) : ", searchObj.group(3)
else:
   print "No search result!!"

printBreakLine()
# re.sub(pattern, repl, string, count=0, flags=0)
# 	pattern : 正则中的模式字符串。
# 	repl : 替换的字符串，*也可为一个函数*。
# 	string : 要被查找替换的原始字符串。
# 	count : 模式匹配后替换的最大次数，默认 0 表示替换所有的匹配。

phone = "2004-959-559 # 这是一个国外电话号码"
 
# 删除字符串中的 Python注释 
num = re.sub(r'#.*$', "", phone)
print "电话号码是: ", num
 
# 删除非数字(-)的字符串 
num = re.sub(r'\D', "", phone)
print "电话号码是 : ", num
printBreakLine()
