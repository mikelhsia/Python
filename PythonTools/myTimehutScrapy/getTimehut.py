import requests
import json
import sys
import os
from datetime import datetime, timedelta

import timehutDataSchema
import timehutManageLastUpdate
import timehutLog
import timehutSeleniumToolKit
import timehutManageDB

PEEKABOO_ONON_ID = "537413380"
PEEKABOO_MUIMUI_ID = "537776076"
PEEKABOO_DB_NAME= "peekaboo"
PEEKABOO_LOGIN_PAGE_URL= "https://www.shiguangxiaowu.cn/zh-CN"
PEEKABOO_HEADLESS_MODE= False

RABBITMQ_PS_CMD = "ps -ef | grep rabbitmq-server | grep sbin | grep -v grep | awk '{print $2}'"

ENABLE_DB_LOGGING = False


# TODO Move these codes to consumer
# TODO Cleaning the info.logging
# functions
def timestampToDatetimeString(ts):
	"""
	Convert timestamp into string with datetime format
	:param ts: timestamp
	:return: datetime string
	"""
	if isinstance(ts, (int, float, str)):
		try:
			ts = int(ts)
		except ValueError:
			raise ValueError

		if len(str(ts)) == 13:
			ts = int(ts / 1000)
		if len(str(ts)) != 10:
			raise ValueError
	else:
		raise ValueError

	return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M%:%S")


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
			# print(c_rec)

		elif data['layout'] == 'milestone':
			continue

		else:
			print(data)
			raise TypeError

	return collection_list


def parseMomentBody(response_body):
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
		# print(m_rec)

	return moment_list


def main(baby, days):
	# main function()
	try:
		__before_day = int(days)
	except Exception as e:
		__before_day = -200
		# __before_day = 3000

	if baby == '1' or baby == '':
		__baby_id = PEEKABOO_ONON_ID
	else:
		# Mui Mui Baby ID
		__baby_id = PEEKABOO_MUIMUI_ID

	last_update_manager = timehutManageLastUpdate.LastUpdateTsManager()
	last_updated_time = last_update_manager.readLastUpdateTimeStamp(__baby_id)

	timehutManageDB.createDB(PEEKABOO_DB_NAME, timehutDataSchema.base, ENABLE_DB_LOGGING)
	__engine = timehutManageDB.createEngine(PEEKABOO_DB_NAME, ENABLE_DB_LOGGING)
	__session = timehutManageDB.createSession(__engine)
	collection_index_list, moment_index_list = timehutManageDB.generateIndexList(__session)

	__timehut = timehutSeleniumToolKit.timehutSeleniumToolKit(PEEKABOO_HEADLESS_MODE)
	__timehut.fetchTimehutLoginPage(PEEKABOO_LOGIN_PAGE_URL)

	if not __timehut.loginTimehut('mikelhsia@hotmail.com', 'f19811128'):
		timehutLog.logging.info('Login failed')
		print('Login failed')
	else:
		timehutLog.logging.info('Login success')
		print('Login success')

		if baby == '1' or baby == '':
			print('Going to Onon')
		else:
			print('Going to MuiMui')
			mui_mui_homepage = __timehut.getTimehutPageUrl().replace(PEEKABOO_ONON_ID, PEEKABOO_MUIMUI_ID)
			__timehut.fetchTimehutContentPage(mui_mui_homepage)

		__collection_list = []
		memory_set = set()
		__cont_flag = True

		# TODO Using Queue instead of using while loop
		while __cont_flag:
			print('start scroll down')
			__timehut.scrollDownTimehutPage()
			print('Done scroll down')

			print('start record')
			__req_list = __timehut.getTimehutRecordedCollectionRequest()
			print('done record')
			print(f'start replay: {__req_list}')
			__res_list, __cont_flag = __timehut.replayTimehutRecordedCollectionRequest(__req_list, __before_day)
			print(f'done replay, cont_flag = {__cont_flag}')

			for __res in __res_list:
				print('start parsing')
				__collection_list = parseCollectionBody(__res)
				print('done parsing')

				print('start update DB')
				timehutManageDB.updateDBCollection(__collection_list, collection_index_list, last_updated_time, __session)
				print('Done update DB')

			# TODO: Replace the old set with the new set? Need to check
			memory_set = __timehut.getTimehutAlbumURLSet()
			__timehut.cleanTimehutRecordedRequest()

		# Start dumping all memories after finish updating Collection
		print('\n-------------------------------\nDone updating collection\nparsing memory set')
		for memory_link in memory_set:
			print(f'memory_link: {memory_link}')
			print('start fecthing')
			__timehut.fetchTimehutContentPage(memory_link)
			print('done fecthing')

			__req_list = __timehut.getTimehutRecordedMomeryRequest()
			__timehut.cleanTimehutRecordedRequest()

			print('start replay')
			__res_list = __timehut.replayTimehutRecordedMemoryRequest(__req_list)
			print('done replay')

			for memory in __res_list:
				print('start parsing')
				moment_list = parseMomentBody(memory)
				print('done parsing')
				print('start update DB')
				timehutManageDB.updateDBMoment(moment_list, moment_index_list, last_updated_time, __session)
				print('done update DB')
				# print(moment_list)

	__timehut.quitTimehutPage()
	timehutManageDB.closeSession(__session)

	# Found out that actually the time that timehut using is actually UTC-0, therefore minus 8 hours
	last_update_manager.writeLastUpdateTimeStamp((datetime.now() + timedelta(hours=-8)).timestamp(), __baby_id)


# TODO: Refactoring const
# TODO: Checking RabbitMQ is running or not
# TODO: Implement RabbitMQ with direct exchange type
# TODO: TBD

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
		timehutLog.logging.info(f'RabbitMQ is running ... ')
	else:
		sys.stdout.write(f"Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first")
		timehutLog.logging.error(f'Error: RabbitMQ is not running. Please run `sudo rabbit-mq` on the server first')
		sys.exit(1)

	'''
	lauch_receiver_worker()

	main_logic_with_sending_to_queue()
	'''

	baby = input(f'Do you want to get data for \n1) Anson or \n2) Angie\n')
	days = input(f'What days you would like to stop at: \n -200 (default) ~ XXXXX:\n')
	main(baby, days)
