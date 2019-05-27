import pika
import sys


severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
print(f'{severity}:{sys.argv[1]}:{len(sys.argv)}')
message = ' '.join(sys.argv[2:]) or 'info: Hello World!'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
# channel.basic_publish(exchange='logs', routing_key='', body=message)
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)

print(f' [x] Sent {severity}:{message}')

connection.close()
