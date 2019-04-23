import sys
import os
import re
import pika
import json

import timehutLog
import timehutSeleniumToolKit

# import pdb
# pdb.set_trace()

PEEKABOO_ONON_ID = "537413380"
PEEKABOO_MUIMUI_ID = "537776076"
PEEKABOO_DB_NAME= "peekaboo"
PEEKABOO_LOGIN_PAGE_URL= "https://www.shiguangxiaowu.cn/zh-CN"
PEEKABOO_HEADLESS_MODE= False
PEEKABOO_COLLECTION_REQUEST = 'collection'
PEEKABOO_MOMENT_REQUEST = 'moment'

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"
RABBITMQ_SERVICE_DEV_URL = 'localhost'
RABBITMQ_TIMEHUT_QUEUE_NAME = 'timehut_queue'


# TODO Cleaning the info.logging

def enqueue_timehut_collection(channel, req_list, before_day=-200):
	next_flag = False

	for request in req_list:
		regex = r'.*&before\=(\d*).*'
		result = re.match(regex, request[0])

		if result is not None:
			before = int(result.group(1))
		else:
			before = 3000

		print(f'before: {before}, before_day: {before_day}')
		if before >= before_day:
			next_flag = True
		else:
			next_flag = False
			break

		print(f'{type(request[0])}: {request[0]}')
		print(f'{type(request[1])}: {request[1]}')
		message = {
			"type": PEEKABOO_COLLECTION_REQUEST,
			"request": request[0],
			"header": json.dumps(request[1].__str__().replace("'", "\""))}

		channel.basic_publish(exchange="", routing_key=RABBITMQ_TIMEHUT_QUEUE_NAME,
		                      body=json.dumps(message).encode('UTF-8'),
		                      properties=pika.BasicProperties(delivery_mode=2,
		                                                      content_type='application/json',
		                                                      content_encoding='UTF-8'))

	return next_flag


def enqueue_timehut_moment(channel, req_list):
	for request in req_list:
		message = {
			"type": PEEKABOO_MOMENT_REQUEST,
			"request": request[0],
			"header": json.dumps(request[1].__str__().replace("'", "\""))}

		channel.basic_publish(exchange="", routing_key=RABBITMQ_TIMEHUT_QUEUE_NAME,
		                      body=json.dumps(message).encode('UTF-8'),
		                      properties=pika.BasicProperties(delivery_mode=2,
		                                                      content_type='application/json',
		                                                      content_encoding='UTF-8'))


def main(baby, days):
	try:
		__before_day = int(days)
	except Exception as e:
		__before_day = -200
		timehutLog.logging.warning(f"before_day format invalid: {type(__before_day)}")

	if baby == '1' or baby == '':
		__baby_id = PEEKABOO_ONON_ID
	else:
		__baby_id = PEEKABOO_MUIMUI_ID

	__timehut = timehutSeleniumToolKit.timehutSeleniumToolKit(PEEKABOO_HEADLESS_MODE)
	__timehut.fetchTimehutLoginPage(PEEKABOO_LOGIN_PAGE_URL)

	if not __timehut.loginTimehut('mikelhsia@hotmail.com', 'f19811128'):
		timehutLog.logging.info('Login failed')
		sys.exit(1)
	else:
		sys.stdout.write('Login success\n')

		if baby == '1' or baby == '':
			sys.stdout.write('Going to Onon\n')
		else:
			sys.stdout.write('Going to MuiMui\n')
			mui_mui_homepage = __timehut.getTimehutPageUrl().replace(PEEKABOO_ONON_ID, PEEKABOO_MUIMUI_ID)
			__timehut.fetchTimehutContentPage(mui_mui_homepage)

		__collection_list = []
		# TODO Can be removed?
		memory_set = set()
		__cont_flag = True

		connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVICE_DEV_URL))
		channel = connection.channel()
		channel.queue_declare(queue=RABBITMQ_TIMEHUT_QUEUE_NAME, durable=True)

		while __cont_flag:
			print('start scroll down')
			__timehut.scrollDownTimehutPage()

			print('start record')
			__req_list = __timehut.getTimehutRecordedCollectionRequest()

			# TODO bear in mind how to stop and detect the last request
			# Send to queue
			__cont_flag = enqueue_timehut_collection(channel, __req_list)

			memory_set = __timehut.getTimehutAlbumURLSet()
			__timehut.cleanTimehutRecordedRequest()

		# Start dumping all memories after finish updating Collection
		print('\n-------------------------------\nDone updating collection, start parsing memory set')

		for memory_link in memory_set:
			print('start fetching')
			__timehut.fetchTimehutContentPage(memory_link)

			__req_list = __timehut.getTimehutRecordedMomeryRequest()
			__timehut.cleanTimehutRecordedRequest()

			# Send to queue
			enqueue_timehut_moment(channel, __req_list)

	__timehut.quitTimehutPage()


def check_rabbit_exist():
	rabbit_result = ''
	timehutLog.logging.info(f'Checking RabbitMQ ... ')
	with os.popen(RABBITMQ_PS_CMD, "r") as f:
		rabbit_result = f.read()

	f.close()

	return False if not rabbit_result else True


# Basic interactive interface
if __name__ == "__main__":

	if check_rabbit_exist():
		sys.stdout.write(f'RabbitMQ is running ... \n')
	else:
		sys.stderr.write(f"RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first\n")
		sys.exit(1)

	baby = input(f'Do you want to get data for \n1) Anson or \n2) Angie\n')
	days = input(f'What days you would like to stop at: \n -200 (default) ~ XXXXX:\n')
	main(baby, days)
