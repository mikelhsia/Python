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
print(fp.fileName)


############################
# 自定义容器的magic method
############################
# 下面细致了解下定义容器可能用到的魔术方法。
# 首先，实现不可变容器的话，你只能定义 __len__ 和 __getitem__ (下面会讲更多)。
# 可变容器协议则需要所有不可变容器的所有，另外还需要 __setitem__ 和 __delitem__。
# 如果你希望你的对象是可迭代的话，你需要定义 __iter__ 会返回一个迭代器。
# 迭代器必须遵循迭代器协议，需要有 __iter__(返回它本身) 和 next。
# __len__(self)
# __getitem__(self, key)
# __setitem__(self, key, value)
# __delitem__(self, key)
# __iter__(self)              # 返回一个容器迭代器，很多情况下会返回迭代器，尤其是当内置的iter()方法被调用的时候，
#                             # 以及当使用for x in container:方式循环的时候。迭代器是它们本身的对象，它们必须定义返回self的__iter__方法。
# __reversed__(self)
# __contains__(self, item)    # 定义了调用in和not in来测试成员是否存在的时候所产生的行为。
# __missing__(self, key)      # 它定义了key如果在容器中找不到时触发的行为
# __instancecheck__(self, instance)     # 检查一个实例是不是你定义的类的实例
# __subclasscheck__(self, subclass)     # 检查一个类是不是你定义的类的子类

class FunctionalList():
	def __init__(self, values=None):
		if values is None:
			self.values = []
		else:
			self.values = values

	def __len__(self):
		return len(self.values)

	def __getitem__(self, item):
		return self.values[item]

	def __setitem__(self, key, value):
		self.values[key] = value

	def __delitem__(self, key):
		del self.values[key]

	def __iter__(self):
		return iter(self.values)

	def __reversed__(self):
		return FunctionalList(reversed(self.values))

	def append(self, value):
		self.values.append(value)

	def head(self):
		# 获取第一个元素
		return self.values[0]

	def tail(self):
		# 获取第一个元素之后的所有元素
		return self.values[1:]

	def init(self):
		# 获取最后一个元素之前的所有元素
		return self.values[:-1]

	def last(self):
		# 获取最后一个元素
		return self.values[-1]

	def drop(self, n):
		# 获取所有元素，除了前N个
		return self.values[n:]

	def take(self, n):
		# 获取前N个元素
		return self.values[:n]



############################
# 可调用的对象
# __call__(self, [args...])
############################
# 允许一个类的实例像函数一样被调用。实质上说，这意味着 x() 与 x.__call__() 是相同的。
# 注意 __call__ 的参数可变。这意味着你可以定义 __call__ 为其他你想要的函数，无论有多少个参数。

class Entity:
	"""
	调用实体来改变实体的位置
	"""
	def __init__(self, size, x, y):
		self.x, self.y = x, y
		self.size = size

	def __call__(self, x, y):
		"""
		改变实体的位置
		"""
		self.x, self.y = x, y


############################
# 上下文管理
############################
# 在with声明的代码段中，我们可以做一些对象的开始操作和退出操作,还能对异常进行处理。这需要实现两个魔术方法: __enter__ 和 __exit__。
# __enter__(self)
#       定义了当使用with语句的时候，会话管理器在块被初始创建时要产生的行为。
#		请注意，__enter__的返回值与with语句的目标或者as后的名字绑定。
# __exit__(self, exception_type, exception_value, traceback)
#       定义了当一个代码块被执行或者终止后，会话管理器应该做什么。
#		它可以被用来处理异常、执行清理工作或做一些代码块执行完毕之后的日常工作。
#		如果代码块执行成功，exceptiontype，exceptionvalue，和traceback将会为None。
#		否则，你可以选择处理这个异常或者是直接交给用户处理。如果你想处理这个异常的话，
#		请确保__exit在所有语句结束之后返回True。如果你想让异常被会话管理器处理的话，那么就让其产生该异常


############################
# 描述器
############################
# 为了成为一个描述器，一个类必须至少有__get__，__set__，__delete__方法被实现：
#
# __get__(self, instance, owner)
# 定义了当描述器的值被取得的时候的行为。instance是拥有该描述器对象的一个实例。owner是拥有者本身
#
# __set__(self, instance, value)
# 定义了当描述器的值被改变的时候的行为。instance是拥有该描述器类的一个实例。value是要设置的值。
#
# __delete__(self, instance)
# 定义了当描述器的值被删除的时候的行为。instance是拥有该描述器对象的一个实例。


############################
# 复制
############################
# 有时候，尤其是当你在处理可变对象时，你可能想要复制一个对象，然后对其做出一些改变而不希望影响原来的对象。
# 这就是Python的copy所发挥作用的地方。
#
# __copy__(self)
# 定义了当对你的类的实例调用copy.copy()时所产生的行为。copy.copy()返回了你的对象的一个浅拷贝——这意味着，
# 当实例本身是一个新实例时，它的所有数据都被引用了——例如，当一个对象本身被复制了，它的数据仍然是被引用的
# （因此，对于浅拷贝中数据的更改仍然可能导致数据在原始对象的中的改变）。

# __deepcopy__(self, memodict={})
# 定义了当对你的类的实例调用copy.deepcopy()时所产生的行为。copy.deepcopy()
# 返回了你的对象的一个深拷贝——对象和其数据都被拷贝了。memodict是对之前被拷贝的对象的一个缓存
# ——这优化了拷贝过程并且阻止了对递归数据结构拷贝时的无限递归。当你想要进行对一个单独的属性进行深拷贝时，
# 调用copy.deepcopy()，并以memodict为第一个参数。