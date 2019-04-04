import pika
import sys


def callback(ch, method, properties, body):
    print(f' [x] {method.routing_key}:{body}')


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 1. whenever we connect to Rabbit we need a fresh, empty queue. To do it we could create a queue with a random name
# 2. Once the consumer connection is closed, the queue should be deleted. Use 'exclusive' flag
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write(f"Usage: {sys.argv[0]} [info] [warning] [error]\n")
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

# channel.queue_bind(exchange='logs', queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
