import pika
import time


# If multiple receiver are activated, it's default round-robin dispatching
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(f' [x] Done')
    # Acknowledge the task is completed
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

# This tells RabbitMQ not to give more than one message to a worker at a time.
# Or, in other words, don't dispatch a new message to a worker until it has processed
# and acknowledged the previous one.
channel.basic_qos(prefetch_count=1)

# Manual message acknowledgments are turned on by default
# channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
