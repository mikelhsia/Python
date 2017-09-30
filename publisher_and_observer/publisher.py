import itertools

'''
观察者模式实现
'''

class Publisher:
	def __init__(self):
		self.observers = set()

	def add(self, observer, *observers):
		# chain([1, 2, 3], [4, 5, 7])  # 连接两个循环器成为一个。1, 2, 3, 4, 5, 7
		for observer in itertools.chain((observer, ), observers):
			self.observers.add(observer)
			# (取并集，改变原来的集合)
			# 注册新的观察者对象时，观察者的
			# update() 方法会执行，这使得它能够用模型当前的状态初始化自己
			observer.update(self)
		else:
			print('Failed to add: {}'.format(observer))

	def remove(self, observer):
		try:
			self.observers.discard(observer)
		except ValueError:
			print('Failed to remove: {}'.format(observer))

	def notify(self):
		# 模型状态发生变化时，应该调用继承而来的 notify() 方法，这样的话，
		# 就会执行每个观察者对象的 update() 方法，以确保他们都能反映出模型的最新状态。
		[observer.update(self) for observer in self.observers]


class DefaultFormatter(Publisher):

	def __init__(self, name):
		super(DefaultFormatter, self).__init__()
		self.name = name
		self._data = 0

	def __str__(self):
		return "{}: '{}' has data = {}".format(type(self).__name__, self.name, self._data)

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, new_value):
		try:
			self._data = int(new_value)
		except ValueError as e:
			print("Error: {}".format(e))
		else:
			self.notify()

class HexFormatter:

	def update(self, publisher):
		print("{}: '{}' has now hex data= {}".format(type(self).__name__, publisher.name, hex(publisher.data)))

class BinaryFormatter:

	def update(self, publisher):
		print("{}: '{}' has now bin data= {}".format(type(self).__name__, publisher.name, bin(publisher.data)))

def main():
	df = DefaultFormatter('test1')
	print(df, end='\n----------\n')

	hf = HexFormatter()
	df.add(hf)
	df.data = 21
	print(df, end='\n----------\n')

	bf = BinaryFormatter()
	df.add(bf)
	df.data = 21
	print(df, end='\n----------\n')

	df.remove(hf)
	df.data = 40
	print(df, end='\n----------\n')

	df.remove(bf)
	df.data = "Hello!"
	print(df, end='\n----------\n')

	df.data = 4.2
	print(df, end='\n----------\n')

if __name__ == '__main__':
	main()

