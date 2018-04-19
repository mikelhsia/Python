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

def dbconn(fn):
	def wrapper(*args, **kwargs):
		db = Database()

		db.connect()

		ret = fn(db, *args, **kwargs)

		db.close()

		return ret

	return wrapper


@dbconn
def handle_query(db=None):
	print('handle --- ', db.query())


def main():
	handle_query()


if __name__ == '__main__':
	main()