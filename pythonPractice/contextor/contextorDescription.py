'''
上下文管理协议
前面初略的提及了上下文，那什么又是上下文管理器呢？与python黑魔法—迭代器类似，实现了迭代协议的函数/对象即为迭代器。
实现了上下文协议的函数/对象即为上下文管理器。
迭代器协议是实现了__iter__方法。上下文管理协议则是__enter__和__exit__。对于如下代码结构：

class Contextor:

    def __enter__(self):
        pass



    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

contextor = Contextor()

with contextor [as var]:
    with_body
Contextor 实现了__enter__和__exit__这两个上下文管理器协议，当Contextor调用/实例化的时候，
则创建了上下文管理器contextor。类似于实现迭代器协议类调用生成迭代器一样。


配合with语句使用的时候，上下文管理器会自动调用__enter__方法，然后进入运行时上下文环境，
如果有as 从句，返回自身或另一个与运行时上下文相关的对象，值赋值给var。当with_body执行完毕
退出with语句块或者with_body代码块出现异常，则会自动执行__exit__方法，并且会把对于的异常参数传递进来。
'''


'''
Python为了更优雅，还专门提供了一个模块用于实现更函数式的上下文管理器用法。
使用contextlib 定义一个上下文管理器函数，通过with语句，database调用生成一个上下文管理器，然后调用函数隐式的__enter__方法，
并将结果通yield返回。最后退出上下文环境的时候，在except代码块中执行了__exit__方法。当然我们可以手动模拟上述代码的执行的细节。
'''
import contextlib

class Database(object):

	def __init__(self):
		self.connected = False

	def connect(self):
		self.connected = True

	def close(self):
		self.connected = False

	def query(self):
		if self.connected:
			return 'query data'
		else:
			raise ValueError('DB not connected ')

	def __enter__(self):
		self.connect()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

@contextlib.contextmanager
def database():
	db = Database()

	try:
		if not db.connected:
			db.connect()
		yield db

	except Exception as e:
		db.close()


def handle_query():
	with database() as db:
		print('handle ---', db.query())