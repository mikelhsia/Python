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
	def __new__(cls, *args, **kwargs):
		print("We're at __new__()")

	def __init__(self, filePath, fileName, fileMode):
		# super(FileObject, self).__init__()
		print("We have created file: {}".format(op.join(filePath, fileName)))
		self.mode = fileMode
		self.fileName = fileName
		self.file = open(op.join(filePath, fileName), 'r+')

	def __del__(self):
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
			print("You're getting strings, which is fine")
		else:
			print("You're getting nothing, Out!")

	def __setattr__(self, name, value):
		pass


fp = FileObject('./', 'xml_sax.py', 'r+')
print(type(fp.mode))
