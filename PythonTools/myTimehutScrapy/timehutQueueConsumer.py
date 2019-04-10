import pika
import time
import json

import timehutManageDB
import timehutDataSchema
from datetime import datetime

RABBIT_SERVICE_DEV_URL = 'localhost'
TIMEHUT_RABBITMQ_QUEUE_NAME = 'timehut_queue'

# TODO 1. Parse response_body
# TODO 2. Add Update DB connection
# TODO 3. Fecth request and headers from the queue instead of fetching result

def DatetimeStringToTimeStamp(string):
	"""
	Convert datetime format into timestamp
	:param ts: string
	:return: timestamp
	"""
	string = string.split('+')[0]
	string = string.split('Z')[0]
	try:
		dt = datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%f")
	except Exception as e:
		print(e)
		raise e

	return dt.timestamp()


def parseCollectionBody(response_body):
	collection_list = []

	response_body = json.loads(response_body)
	data_list = response_body['list']

	for data in data_list:

		if data['layout'] == 'collection' or \
				data['layout'] == 'picture' or \
				data['layout'] == 'video' or \
				data['layout'] == 'text':

			c_rec = timehutDataSchema.Collection(id=data['id_str'],
			                                     baby_id=data['baby_id'],
			                                     created_at=data['taken_at_gmt'],
			                                     updated_at=data['updated_at_in_ts'],
			                                     months=data['months'],
			                                     days=data['days'],
			                                     content_type=timehutDataSchema.CollectionEnum[data['layout']].value,
			                                     caption=data['caption'])

			# Add to return collection obj list
			collection_list.append(c_rec)
			print(c_rec)

		elif data['layout'] == 'milestone':
			continue

		else:
			print(data)
			raise TypeError

	return collection_list


def parseMomentBody(response_body):

	response_body = json.loads(response_body)
	moment_list = []
	data_list = response_body['moments']
	src_url = ''

	for data in data_list:
		if data['type'] == 'picture':
			src_url = data['picture']
		elif data['type'] == 'video':
			src_url = data['video_path']

		m_rec = timehutDataSchema.Moment(id=data['id_str'],
		                                 event_id=data['event_id_str'],
		                                 baby_id=data['baby_id'],
		                                 created_at=data['taken_at_gmt'],
		                                 updated_at=DatetimeStringToTimeStamp(data['updated_at']),
		                                 content_type=timehutDataSchema.MomentEnum[data['type']].value,
		                                 content=data['content'],
		                                 src_url=src_url,
		                                 months=data['months'],
		                                 days=data['days'])

		# Add to return collection obj list
		moment_list.append(m_rec)
		print(m_rec)

	return moment_list


def callback(ch, method, properties, body):
	# print(f' [x] Receive {body}')
	text = json.loads(body)

	if text["type"] == "collection":
		print(f' [x] Receive collection')
		parseCollectionBody(text["header"])
	else:
		print(f' [x] Receive moment')
		parseMomentBody(text["header"])

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
