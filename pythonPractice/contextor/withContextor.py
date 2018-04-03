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

def handle_query():
	with Database() as db:
		print('handle ---', db.query())


def main():
	handle_query()


if __name__ == '__main__':
	main()