import requests
import json
import sys
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import InternalError

import timehutDataSchema
import timehutManageLastUpdate
import timehutLog
import timehutSeleniumToolKit


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


def getCollectionRequest(baby_id, before_day):
	"""
	Get collection information through GET request by before day, getting limited collection (around 20)
	:param baby_id: baby ID
	:param before_day: the days of the collection and moment
	:return: Response body of collection information
	"""
	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cookie': 'locale=en;user_session=BAhJIj1qcF81MzY5MjMzNjNfM0JyZDJlNV9LbkJ1OGtqdkRqSHM4UmZyVk1CVUk4a3BrY1JRME9ZVzc1dwY6BkVU--fcb138d8ae1fcb3290cbbd7c4b35101f61d8b40e',
	}

	try:
		r = requests.get(url=f'http://peekaboomoments.com/events.json?baby_id={baby_id}&before={before_day}&v=2&width=700&include_rt=true', headers=headers, timeout=30)
		r.raise_for_status()
	except requests.RequestException as e:
		timehutLog.logging.error(e)
	else:
		response_body = json.loads(r.text)
		timehutLog.logging.info(f"Request fired = {response_body['next']}")
		return response_body['next'], response_body

def getMomentRequest(collection_id):
	"""
	Get moment information through GET request by single collection id
	:param collection_id: collection id
	:return: Response body of moments that belong to the same collection
	"""
	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cookie': 'locale=en;user_session=BAhJIj1qcF81MzY5MjMzNjNfM0JyZDJlNV9LbkJ1OGtqdkRqSHM4UmZyVk1CVUk4a3BrY1JRME9ZVzc1dwY6BkVU--fcb138d8ae1fcb3290cbbd7c4b35101f61d8b40e',
		'X-Requested-With': 'XMLHttpRequest'
	}

	try:
		r = requests.get(url=f'http://peekaboomoments.com/events/{collection_id}', headers=headers, timeout=30)
		r.raise_for_status()
	except requests.RequestException as e:
		timehutLog.logging.error(e)
	else:
		response_body = json.loads(r.text)
		return response_body

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


def createDB(dbName, base, loggingFlag):
	engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306',
	                       encoding='utf-8', echo=loggingFlag)

	try:
		engine.execute(f"CREATE DATABASE IF NOT EXISTS {dbName} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;")
		timehutLog.logging.info(f"CREATE DATABASE IF NOT EXISTS {dbName} DEFAULT CHARSET utf8mb4 COLLATE utf8_general_ci;")

		engine.execute(f"USE {dbName}")
		timehutLog.logging.info(f"USE {dbName}")

		ans = input(f"Do you want to drop the previous saved table (y/N)")

		if ans == 'y' or ans == 'Y':
			engine.execute(f"DROP TABLE {timehutDataSchema.Moment.__tablename__}")
			timehutLog.logging.info(f"DROP TABLE {timehutDataSchema.Moment.__tablename__}")

			engine.execute(f"DROP TABLE {timehutDataSchema.Collection.__tablename__}")
			timehutLog.logging.info(f"DROP TABLE {timehutDataSchema.Collection.__tablename__}")

	except InternalError as e:
		base.metadata.create_all(engine)

		engine.execute(f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")
		engine.execute(f"ALTER TABLE {timehutDataSchema.Collection.__tablename__} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
		engine.execute(f"ALTER TABLE {timehutDataSchema.Collection.__tablename__} MODIFY caption TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
		engine.execute(f"ALTER TABLE {timehutDataSchema.Moment.__tablename__} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
		engine.execute(f"ALTER TABLE {timehutDataSchema.Moment.__tablename__} MODIFY content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")



	engine.dispose()


def createEngine(dbName, base, loggingFlag):

	createDB(dbName, base, loggingFlag)

	engine = create_engine(f'mysql+pymysql://root:hsia0521@127.0.0.1:3306/{dbName}?charset=utf8mb4',
	                       encoding='utf-8', echo=loggingFlag)

	return engine


def generateIndexList(engine):
	DBSession = sessionmaker(bind=engine)
	__session = DBSession()

	__collectionIndexList = []
	__momentIndexList = []

	for row in __session.query(timehutDataSchema.Collection):
		__collectionIndexList.append(row.id)

	for row in __session.query(timehutDataSchema.Moment):
		__momentIndexList.append(row.id)

	return __collectionIndexList, __momentIndexList


def updateDBCollection(data_list, existed_index_list, last_updated_time, session):
	"""

	:param data_list
	:return: 
	"""
	if not isinstance(data_list, list):
		# If it's an single object, then put it in the list to simplify the following logic
		data_list = [data_list]

	for data in data_list:
		if isinstance(data, timehutDataSchema.Collection):
			if data.id not in existed_index_list:
				# Insert collection object
				session.add(data)
			elif data.updated_at > last_updated_time:
				# Update collection object
				session.query(timehutDataSchema.Collection)\
						.filter(timehutDataSchema.Collection.id == data.id)\
						.update({timehutDataSchema.Collection.updated_at: data.updated_at,
								timehutDataSchema.Collection.caption: data.caption})
		else:
			timehutLog.logging.error(f'[{sys._getframe().f_code.co_name}] Wrong Collection Type')
			return False
	else:
		session.commit()


def updateDBMoment(data_list, existed_index_list, last_updated_time, session):
	"""

	:param data_list
	:return: 
	"""
	if not isinstance(data_list, list):
		# If it's an single object, then put it in the list to simplify the following logic
		data_list = [data_list]

	for data in data_list:
		if isinstance(data, timehutDataSchema.Moment):
			if data.id not in existed_index_list:
				# Insert collection object
				session.add(data)
			elif data.updated_at > last_updated_time:
				# Update collection object
				session.query(timehutDataSchema.Moment)\
						.filter(timehutDataSchema.Moment.id == data.id)\
						.update({timehutDataSchema.Moment.updated_at: data.updated_at,
								timehutDataSchema.Moment.content: data.content})
		else:
			timehutLog.logging.error(f'[{sys._getframe().f_code.co_name}] Wrong Moment Type')
			return False
	else:
		session.commit()

# main function()
def main(baby, days):
	try:
		__before_day = int(days)
	except Exception as e:
		__before_day = -200
		# __before_day = 3000

	if baby == '1' or baby == '':
		# On On Baby ID
		__baby_id = 537413380
	else:
		# Mui Mui Baby ID
		__baby_id = 537776076

	last_update_manager = timehutManageLastUpdate.LastUpdateTsManager()
	last_updated_time = last_update_manager.readLastUpdateTimeStamp(__baby_id)

	__dbName = "peekaboo"
	__logging = False
	__engine = createEngine(__dbName, timehutDataSchema.base, __logging)

	collection_index_list, moment_index_list = generateIndexList(__engine)

	DBSession = sessionmaker(bind=__engine)
	__session = DBSession()

	'''
	# These are the old codes that are not valid anymore, as timehut applied token to their APIs
	while (True):
		# Getting original response body and next_index to decide what's the next request to submit
		__next_index, __response_body = getCollectionRequest(__baby_id, __before_day)

		collection_list = parseCollectionBody(__response_body)
		updateDBCollection(collection_list, collection_index_list, last_updated_time, __session)

		for collection in collection_list:
			__response_body = getMomentRequest(collection.id)
			# moment_list = parseMomentBody(__response_body)
			# updateDBMoment(moment_list, moment_index_list, last_updated_time, __session)

		if (__next_index is None):
			break

		__before_day = __next_index + 1
	'''
	__isHeadless = False
	__timehutUrl = "https://www.shiguangxiaowu.cn/zh-CN"

	__timehut = timehutSeleniumToolKit.timehutSeleniumToolKit(True, __isHeadless)

	__timehut.fetchTimehutPage(__timehutUrl)

	if not __timehut.loginTimehut('mikelhsia@hotmail.com', 'f19811128'):
		timehutLog.logging.info('Login failed')
		print('Login failed')
	else:
		timehutLog.logging.info('Login success')
		print('Login success')

		__collection_list = []
		__cont_flag = True

		while __cont_flag:
			print('start scroll down')
			__timehut.scrollDownTimehutPage()
			print('Done scroll down')

			print('start record')
			__req_list = __timehut.getTimehutRecordedCollectionRequest()
			print('done record')
			print('start replay')
			__res_list, __cont_flag = __timehut.replayTimehutRecordedCollectionRequest(__req_list, __before_day)
			print('done replay')
			__timehut.cleanTimehutRecordedCollectionRequest()

			print('start parsing')
			for __res in __res_list:
				__collection_list += parseCollectionBody(__res)
			print('done parsing')

			print('start update DB')
			updateDBCollection(__collection_list, collection_index_list, last_updated_time, __session)
			print('Done update DB')

	__timehut.quitTimehutPage()
	__session.close()

	# Found out that actually the time that timehut using is actually UTC-0, therefore minus 8 hours
	last_update_manager.writeLastUpdateTimeStamp((datetime.now() + timedelta(hours=-8)).timestamp(), __baby_id)


# Basic interactive interface
if __name__ == "__main__":
	baby = input(f'Do you want to get data for \n1) Anson or \n2) Angie\n')
	days = input(f'What days you would like to start with: \n -200 (default) ~ XXXXX:\n')
	main(baby, days)
