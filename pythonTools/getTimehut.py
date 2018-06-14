import requests
import logging
import json
from datetime import datetime

import timehutDataSchema

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(filename='log1.log',
					format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
					datefmt='%Y-%m-%d %H:%M:%S %p',
					level=logging.DEBUG)

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
		logging.error(e)
	else:
		response_body = json.loads(r.text)
		logging.info(f"Request fired = {response_body['next']}")
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
		logging.error(e)
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
			                                   created_at=timestampToDatetimeString(data['taken_at_gmt']),
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
		                                 created_at=timestampToDatetimeString(data['taken_at_gmt']),
		                                 content_type=timehutDataSchema.MomentEnum[data['type']].value,
		                                 content=data['content'],
		                                 src_url=src_url,
		                                 months=data['months'],
		                                 days=data['days'])

		# Add to return collection obj list
		moment_list.append(m_rec)
		print(m_rec)

	return moment_list

def createDB(dbName, base, loggingFlag):
	engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306',
	                       encoding='utf-8', echo=loggingFlag)

	engine.execute(f"CREATE DATABASE IF NOT EXISTS {dbName} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;")
	logging.info(f"CREATE DATABASE IF NOT EXISTS {dbName} DEFAULT CHARSET utf8mb4 COLLATE utf8_general_ci;")

	engine.execute(f"USE {dbName}")
	logging.info(f"USE {dbName}")


	# TODO: It's a stupid way to drop the table everytime. Needs improvement
	# engine.execute(f"DROP TABLE {timehutDataSchema.Collection.__tablename__}")
	# logging.info(f"DROP TABLE {timehutDataSchema.Collection.__tablename__}"))
	#
	# engine.execute(f"DROP TABLE {timehutDataSchema.Moment.__tablename__}")
	# logging.info(f"DROP TABLE {timehutDataSchema.Moment.__tablename__}")

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


# main function()
def main():
	__before_day = -200
	__baby_id = 537413380
	__dbName = "peekaboo"
	__logging = False
	__engine = createEngine(__dbName, timehutDataSchema.base, __logging)
	# DBSession = sessionmaker(bind=__engine)
	# __session = DBSession()

	while (True):
		__next_index, __response_body = getCollectionRequest(__baby_id, __before_day)

		collection_list = parseCollectionBody(__response_body)
		# __session.add_all(collection_list)

		__response_body = getMomentRequest('589886134185628442')
		moment_list = parseMomentBody(__response_body)
		for collection in collection_list:
			# __response_body = getMomentRequest(collection.id)
			# moment_list = parseMomentBody(__response_body)
			# __session.add_all(moment_list)
			pass

		# __session.commit()
		# __session.close()

		if (__next_index is None):
			break

		__before_day = __next_index + 1


# check
if __name__ == "__main__":
	main()
