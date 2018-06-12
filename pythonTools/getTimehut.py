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

memoryCollectionSet = set()
memorySet = set()

# functions
def timestampToDatetimeString(ts):
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

def getRequest(baby_id, before_day):
	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cookie': 'locale=en;user_session=BAhJIj1qcF81MzY5MjMzNjNfM0JyZDJlNV9LbkJ1OGtqdkRqSHM4UmZyVk1CVUk4a3BrY1JRME9ZVzc1dwY6BkVU--fcb138d8ae1fcb3290cbbd7c4b35101f61d8b40e'
	}

	try:
		r = requests.get(url='http://peekaboomoments.com/events.json?baby_id={}&before={}&v=2&width=700&include_rt=true'.format(baby_id, before_day), headers=headers, timeout=30)
		r.raise_for_status()
	except requests.RequestException as e:
		logging.error(e)
	else:
		response_body = json.loads(r.text)
		logging.info("Request fired = {}".format(response_body['next']))
		return response_body['next'], response_body

def parseResponseBody(response_body):
	collection_list = []
	memory_list = []

	data_list = response_body['list']

	for i in range(0, len(data_list)):
		memory_id_list = []

		if data_list[i]['layout'] == 'collection':
			data_list_detail = data_list[i]['layout_detail']

			for j in range(0, len(data_list_detail)):
				src_url =''

				if data_list_detail[j]['type'] == 'picture':
					src_url = data_list_detail[j]['picture']
				if data_list_detail[j]['type'] == 'video':
					src_url = data_list_detail[j]['video_path']

				m_rec = timehutDataSchema.Memory(mid=data_list_detail[j]['id_str'],
				                                 created_at=timestampToDatetimeString(data_list_detail[j]['taken_at_gmt']),
				                                 content_type=timehutDataSchema.MemoryEnum[data_list_detail[j]['type']].value,
				                                 content=data_list_detail[j]['content'],
				                                 src_url=src_url)

				print(m_rec)

				# Add to non-repeatable memory set
				memorySet.add(m_rec.id)

				# Add to return memory obj list
				memory_list.append(m_rec)

				# Add to memorry collection memory list
				memory_id_list.append(data_list_detail[j]['id_str'])

			c_rec = timehutDataSchema.Collection(id=data_list[i]['id_str'],
			                                   baby_id=data_list[i]['baby_id'],
			                                   created_at=timestampToDatetimeString(data_list[i]['taken_at_gmt']),
			                                   months=data_list[i]['months'],
			                                   days=data_list[i]['days'],
			                                   memory_type=timehutDataSchema.CollectionEnum[data_list[i]['layout']].value,
			                                   memory_id_list=','.join(memory_id_list),
			                                   caption=data_list[i]['caption'])

			# Add to non-repeatable collection set
			memoryCollectionSet.add(c_rec.id)

			# Add to return collection obj list
			collection_list.append(c_rec)
			print(c_rec)

		elif data_list[i]['layout'] == 'picture':
			data_list_detail = data_list[i]['layout_detail']

			src_url =''

			if data_list_detail[0]['type'] == 'picture':
				src_url = data_list_detail[0]['picture']
			if data_list_detail[0]['type'] == 'video':
				src_url = data_list_detail[0]['video_path']

			m_rec = timehutDataSchema.Memory(mid=data_list_detail[0]['id_str'],
			                                 created_at=timestampToDatetimeString(data_list_detail[0]['taken_at_gmt']),
			                                 content_type=timehutDataSchema.MemoryEnum[data_list_detail[0]['type']].value,
			                                 content=data_list_detail[0]['content'],
			                                 src_url=src_url)

			# Add to non-repeatable memory set
			memorySet.add(m_rec.id)

			# Add to return memory obj list
			memory_list.append(m_rec)

			# Add to memorry collection memory list
			memory_id_list.append(data_list_detail[0]['id_str'])


			c_rec = timehutDataSchema.Collection(id=data_list[i]['id_str'],
												 baby_id=data_list[i]['baby_id'],
												 created_at=timestampToDatetimeString(data_list[i]['taken_at_gmt']),
												 months=data_list[i]['months'],
												 days=data_list[i]['days'],
												 memory_type=timehutDataSchema.CollectionEnum[data_list[i]['layout']].value,
												 memory_id_list=','.join(memory_id_list),
												 caption=data_list[i]['caption'])

			# Add to non-repeatable collection set
			memoryCollectionSet.add(c_rec.id)

			# Add to return collection obj list
			collection_list.append(c_rec)

			print(m_rec)
			print(c_rec)
		elif data_list[i]['layout'] == 'text':
			data_list_detail = data_list[i]['layout_detail']
			pass
		else:
			continue

	return collection_list, memory_list


def createDB(dbName, base, loggingFlag):
	# engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306', echo=loggingFlag)
	engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306',
	                       encoding='utf-8', echo=loggingFlag)

	engine.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci".format(dbName))
	logging.info("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET utf8mb4 COLLATE utf8_general_ci;".format(dbName))

	engine.execute("USE {}".format(dbName))
	logging.info("USE {}".format(dbName))


	# TODO: It's a stupid way to drop the table everytime. Needs improvement
	engine.execute("DROP TABLE {}".format(timehutDataSchema.Collection.__tablename__))
	logging.info("DROP TABLE {}".format(timehutDataSchema.Collection.__tablename__))

	engine.execute("DROP TABLE {}".format(timehutDataSchema.Memory.__tablename__))
	logging.info("DROP TABLE {}".format(timehutDataSchema.Memory.__tablename__))

	base.metadata.create_all(engine)

	engine.execute("ALTER DATABASE {} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;".format(dbName))
	engine.execute("ALTER TABLE {} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(timehutDataSchema.Collection.__tablename__))
	engine.execute("ALTER TABLE {} MODIFY {} VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(timehutDataSchema.Collection.__tablename__, 'caption'))
	engine.execute("ALTER TABLE {} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(timehutDataSchema.Memory.__tablename__))
	engine.execute("ALTER TABLE {} MODIFY {} VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(timehutDataSchema.Memory.__tablename__, 'content'))


	engine.dispose()


def createEngine(dbName, base, loggingFlag):

	createDB(dbName, base, loggingFlag)

	# engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306', echo=loggingFlag)
	engine = create_engine('mysql+pymysql://root:hsia0521@127.0.0.1:3306/{}?charset=utf8mb4'.format(dbName),
	                       encoding='utf-8', echo=loggingFlag)

	return engine


# main function()
def main():
	__before_day = 100
	__baby_id = 537413380
	__dbName = "peekaboo"
	__logging = False
	__engine = createEngine(__dbName, timehutDataSchema.base, __logging)
	DBSession = sessionmaker(bind=__engine)
	__session = DBSession()

	while (True):
		__next_index, __response_body = getRequest(__baby_id, __before_day)

		collection_list, memory_list = parseResponseBody(__response_body)
		__session.add_all(collection_list)
		__session.add_all(memory_list)
		# TODO sqlalchemy.exc.InternalError: (pymysql.err.InternalError) (1366, "Incorrect string value:
		# '\\xF0\\x9F\\xA4\\x98\\xF0\\x9F...' for column 'caption' at row 4")
		__session.commit()
		__session.close()

		if (__next_index is None):
			break

		__before_day = __next_index + 1


# check
if __name__ == "__main__":
	main()
