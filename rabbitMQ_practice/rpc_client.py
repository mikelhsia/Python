import pika
import uuid

class FibonacciRpcClient(object):
	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		self.channel = self.connection.channel()

		result = self.channel.queue_declare('', exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_reponse, auto_ack=True)

	def on_reponse(self, ch, method, props, body):
		# The 'on_response' callback executed on every response is doing a very simple job,
		# for every response message it checks if the correlation_id is the one we're looking for.
		# If so, it saves the response in self.response and breaks the consuming loop.
		if self.corr_id == props.correlation_id:
			self.response = body

	def call(self, n):
		'''
		Main call method, that does the actual RPC request
		:param n:
		:return:
		'''
		self.response = None
		self.corr_id = str(uuid.uuid4())
		'''
		Message Properties
		The AMQP 0-9-1 protocol predefines a set of 14 properties that go with a message. 
		Most of the properties are rarely used, with the exception of the following:
			- delivery_mode: Marks a message as persistent (with a value of 2) or transient 
						(any other value). You may remember this property from the second tutorial.
			- content_type: Used to describe the mime-type of the encoding. For example for 
						the often used JSON encoding it is a good practice to set this property 
						to: application/json.
			- reply_to: Commonly used to name a callback queue.
			- correlation_id: Useful to correlate RPC responses with requests.
		'''
		self.channel.basic_publish(exchange='', routing_key='rpc_queue',
		                           properties=pika.BasicProperties(reply_to=self.callback_queue,
		                                                           correlation_id=self.corr_id),
		                           body=str(n))

		while self.response is None:
			self.connection.process_data_events()

		return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(f' [x] Requesting fib(30)')
response = fibonacci_rpc.call(30)
print(f' [.] Got {response}')
