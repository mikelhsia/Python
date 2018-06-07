import requests
import json

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class MemoryCollection:
	def __init__(self, id, baby_id, created_at, months, days, layout, caption, obj):
		self.id = id
		self.baby_id = baby_id
		self.created_at = created_at
		self.months = months
		self.days = days
		self.layout = layout
		self.layout_id_list = []
		self.caption = caption
		self.memory = Memory(obj)

	def store(self):
		pass

class Memory:
	def __init__(self, id, content, photo_path, video_path):
		self.id = id
		self.content = content
		self.src_url = video_path if video_path else photo_path

	def store(self):
		pass

memoryCollectionSet = set()
memorySet = set()

before_day = 3000

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cookie': 'locale=en;user_session=BAhJIj1qcF81MzY5MjMzNjNfM0JyZDJlNV9LbkJ1OGtqdkRqSHM4UmZyVk1CVUk4a3BrY1JRME9ZVzc1dwY6BkVU--fcb138d8ae1fcb3290cbbd7c4b35101f61d8b40e'
}

r = requests.get(url='http://peekaboomoments.com/events.json?baby_id=537413380&before={}&v=2&width=700&include_rt=true'.format(before_day), headers=headers)

obj_list = json.loads(r.text)['list']

engine = create_engine('mysql+pymysql://root:michael0512@127.0.0.1:3306/php_test')
