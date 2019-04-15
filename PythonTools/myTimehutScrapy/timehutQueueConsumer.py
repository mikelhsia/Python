import pika
import time
import json
import requests
import os
import sys

import timehutLog
import timehutManageDB
import timehutDataSchema
from datetime import datetime

# import pdb
# pdb.set_trace()

RABBIT_SERVICE_DEV_URL = 'localhost'
TIMEHUT_RABBITMQ_QUEUE_NAME = 'timehut_queue'

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"

# TODO 2. Add Update DB connection


class timehutQueueConsumer(object):
	def __init__(self):
		pass

	def DatetimeStringToTimeStamp(self, string):
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


	def parseCollectionBody(self, response_body):
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


	def parseMomentBody(self, response_body):

		moment_list = []
		response_body = json.loads(response_body)
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
											 updated_at=self.DatetimeStringToTimeStamp(data['updated_at']),
											 content_type=timehutDataSchema.MomentEnum[data['type']].value,
											 content=data['content'],
											 src_url=src_url,
											 months=data['months'],
											 days=data['days'])

			# Add to return collection obj list
			moment_list.append(m_rec)
			print(m_rec)

		return moment_list

	# def onMessageCallback(ch, method, properties, body):
	def onMessageCallback(self, ch, method, properties, body):
		# print(f' [x] Receive {body}')
		text = json.loads(body)

		if text["type"] == "collection":
			print(f' [x] Receive collection')
			request = text["request"]
			# 将字符串转换为字典
			header = eval(json.loads(text["header"]))

			try:
				r = requests.get(url=request, headers=header, timeout=30)
				r.raise_for_status()
			except requests.RequestException as e:
				print(f'{e}')
			else:
				self.parseCollectionBody(r.text)
		else:
			print(f' [x] Receive moment')
			request = text["request"]
			# 将字符串转换为字典
			header = eval(json.loads(text["header"]))

			try:
				r = requests.get(url=request, headers=header, timeout=30)
				r.raise_for_status()
			except requests.RequestException as e:
				print(f'{e}')
			else:
				self.parseMomentBody(r.text)

		print(f' [x] Done')
		ch.basic_ack(delivery_tag=method.delivery_tag)


	def onChannelCloseCallback(self):
		pass
		# timehutManageDB.closeSession(__session)

	def onChannelOpenCallback(self):
		# timehutManageDB.createDB(PEEKABOO_DB_NAME, timehutDataSchema.base, ENABLE_DB_LOGGING)
		# __engine = timehutManageDB.createEngine(PEEKABOO_DB_NAME, ENABLE_DB_LOGGING)
		# __session = timehutManageDB.createSession(__engine)
		# collection_index_list, moment_index_list = timehutManageDB.generateIndexList(__session)
		pass

	def run(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVICE_DEV_URL))
		channel = connection.channel()

		channel.queue_declare(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, durable=True)
		print(f' [*] Waiting for message. To exit press CTRL+C')

		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(queue=TIMEHUT_RABBITMQ_QUEUE_NAME, on_message_callback=self.onMessageCallback)

		channel.start_consuming()


def check_rabbit_exist():
	rabbit_result = ''
	timehutLog.logging.info(f'Checking RabbitMQ ... ')
	with os.popen(RABBITMQ_PS_CMD, "r") as f:
		rabbit_result = f.read()

	f.close()

	return False if not rabbit_result else True


if __name__ == "__main__":

	if check_rabbit_exist():
		timehutLog.logging.info(f'RabbitMQ is running ... ')
	else:
		sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first")
		timehutLog.logging.error(f'Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first')
		sys.exit(1)

	queueConsumer = timehutQueueConsumer()
	queueConsumer.run()
