import pika
import time
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InternalError

import timehutDataSchema

RABBIT_SERVICE_DEV_URL = 'localhost'
TIMEHUT_RABBITMQ_QUEUE_NAME = 'timehut_queue'


def callback(ch, method, properties, body):
	print(f' [x] Receive {body}')
	text = json.loads(body)

	if text["type"] == "collection":
		print(f' [x] Receive collection {text["header"]}')
	else:
		print(f' [x] Receive moment {text["header"]}')

	time.sleep(int(text["request"]))
	print(f' [x] Done')
	ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVICE_DEV_URL))
channel = connection.channel()

channel.queue_declare(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, durable=True)
print(f' [*] Waiting for message. To exit press CTRL+C')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, on_message_callback=callback)

channel.start_consuming()
