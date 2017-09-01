#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
'''
在Python中，所有以“__”双下划线包起来的方法，都统称为“Magic Method”,
例如类的初始化方法 __init__,Python中所有的魔术方法均在官方文档中有相应描述，
但是对于官方的描述比较混乱而且组织比较松散。很难找到有一个例子。
'''

# 每个Pythoner都知道一个最基本的魔术方法， __init__ 。通过此方法我们可以定义一个对象的初始操作。
# 然而，当调用 x = SomeClass() 的时候， __init__ 并不是第一个被调用的方法。
# 实际上，还有一个叫做__new__ 的方法，两个共同构成了“构造函数”。
# __new__是用来创建类并返回这个类的实例, 而__init__只是将传入的参数来初始化该实例。
# 在对象生命周期调用结束时，__del__ 方法会被调用，可以将__del__理解为“构析函数”
from os import path as op

class FileObject(object):
	'''给文件对象进行包装从而确认在删除时文件流关闭'''
	# def __new__(cls, *args, **kwargs):
		# print("We're at __new__()")

	def __init__(self, filePath, fileName, fileMode):
		# super(FileObject, self).__init__()
		print("We have opened the file: {}".format(op.join(filePath, fileName)))
		self.mode = fileMode
		self.fileName = fileName
		self.file = open(op.join(filePath, fileName), 'r+')

	def __del__(self):
		print("-------------")
		print("Start cleaning up")
		self.file.close()
		del self.file

		try:
			self.file.close()
		except:
			print("File has been closed successfully")

	# 定义当用户试图获取一个不存在的属性时的行为。这适用于对普通拼写错误的获取和重定向，
	# 对获取一些不建议的属性时候给出警告(如果你愿意你也可以计算并且给出一个值)或者处理一个 AttributeError 。
	# 只有当调用不存在的属性的时候会被返回。
	def __getattr__(self, itemName):
		if type(itemName) is str:
			print("You're getting strings:{}, which is fine".format(itemName))
		else:
			print("You're getting nothing, Out!")

	# 与__getattr__(self, name) 不同，__setattr__ 是一个封装的解决方案。无论属性是否存在，
	# 它都允许你定义对对属性的赋值行为，以为这你可以对属性的值进行个性定制。实现__setattr__时要避免”无限递归”的错误。
	# def __setattr__(self, name, value):
	# 	pass
	############################
	# #  错误用法
	# def __setattr__(self, name, value):
	# 	self.name = value
	# # 每当属性被赋值的时候(如self.name = value)， ``__setattr__()`` 会被调用，这样就造成了递归调用。
	# # 这意味这会调用 ``self.__setattr__('name', value)`` ，每次方法会调用自己。这样会造成程序崩溃。
	#
	# #  正确用法
	# def __setattr__(self, name, value):
	# 	self.__dict__[name] = value  # 给类中的属性名分配值
	# # 定制特有属性
	############################

	# 与 __setattr__ 相同，但是功能是删除一个属性而不是设置他们。实现时也要防止无限递归现象发生。
	# def __delattr__(self, item):
	# 	pass

	# __getattribute__定义了你的属性被访问时的行为，相比较，__getattr__只有该属性不存在时才会起作用。
	# 因此，在支持__getattribute__的Python版本, 调用__getattr__前必定会调用 __getattribute__。
	# __getattribute__同样要避免”无限递归”的错误。需要提醒的是，最好不要尝试去实现__getattribute__,
	# 因为很少见到这种做法，而且很容易出bug。
	# def __getattribute__(self, item):
	# 	print("Before getting the attribute")



fp = FileObject('./', 'xml_sax.py', 'r+')
print fp.fileName
