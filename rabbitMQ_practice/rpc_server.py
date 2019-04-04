import pika
import sys

'''
Our RPC will work like this:

- When the Client starts up, it creates an anonymous exclusive callback queue.
- For an RPC request, the Client sends a message with two properties: reply_to,
	which is set to the callback queue and correlation_id, which is set to a 
	unique value for every request.
- The request is sent to an rpc_queue queue.
- The RPC worker (aka: server) is waiting for requests on that queue. When a 
	request appears, it does the job and sends a message with the result back 
	to the Client, using the queue from the reply_to field.
- The client waits for data on the callback queue. When a message appears, it 
	checks the correlation_id property. If it matches the value from the request 
	it returns the response to the application.
'''

def fib(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
	'''
	We declare a callback for basic_consume, the core of the RPC server.
	It's executed when the request is received. It does the work and sends the response back.
	:param ch: Channel
	:param method: Method
	:param props: Properties
	:param body: Message body
	:return: [optional]
	'''
	try:
		n = int(body)
	except Exception:
		n = 1
		sys.stderr.write(f'Wrong Fib data type. Setting to default 1')

	print(f' [.] fib({n})')
	response = fib(n)
	ch.basic_publish(exchange='',
					 routing_key=props.reply_to,
					 properties=pika.BasicProperties(correlation_id=props.correlation_id),
					 body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

# We might want to run more than one server process. In order to spread the load equally over multiple
# servers we need to set the prefetch_count setting.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(f' [x] Awaiting RPC requests')

channel.start_consuming()
