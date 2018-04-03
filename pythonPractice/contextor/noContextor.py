'''
本文所讨论的上下文，简而言之，就是程式所执行的环境状态，或者说程式运行的情景。
关于上下文的定义，具体通过程式来理解。既然提及上下文，就不可避免的涉及Python中关于上下文的魔法，即上下文管理器（contextor）。
上下文管理器的常用于一些资源i操作，需要在资源的获取与释放相关的操作，一个典型的例子就是数据库的连接，查询，关闭处理。先看如下一个例子：

代码可以work，可是如果很多地方有类似handle_query的逻辑，连接和关闭这样的代码就得copy很多遍，显然不是一个优雅的设计。
'''
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


def handle_query():
	db = Database()

	db.connect()

	print('handle --- ', db.query())

	db.close()


def main():
	handle_query()


if __name__ == '__main__':
	main()