from sqlalchemy import Column, String, Integer, DateTime, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

import enum
class CollectionEnum(enum.Enum):
	collection = 1
	text = 2
	picture = 3
	video = 4

class MemoryEnum(enum.Enum):
	text = 1
	rich_text = 2
	picture = 3
	video = 4

base = declarative_base()

class Collection(base):
	__tablename__ = 'peekaboo_collection'

	id = Column(String(32), primary_key=True)
	baby_id = Column(String(32))
	created_at = Column(DateTime)
	months = Column(Integer)
	days = Column(Integer)
	memory_type = Column(SmallInteger)
	memory_id_list = Column(Text)
	caption = Column(Text)

	def __repr__(self):
		return '---- Collection ----\n' \
		       'id: {}\n' \
		       'baby_id: {}\n' \
		       'created_at: {}\n' \
		       'months: {} \n' \
		       'days: {} \n' \
		       'memory_type: {}\n' \
		       'memory_id_list: {}\n' \
		       'caption: {} \n' \
		       '--------------------'\
			.format(self.id,
		         self.baby_id,
		         self.created_at,
		         self.months,
		         self.days,
		         self.memory_type,
		         self.memory_id_list,
		         self.caption)



class Memory(base):
	__tablename__ = 'peekaboo_memory'

	id = Column(Integer, primary_key=True, autoincrement=True)
	mid = Column(String(32), unique=True)
	created_at = Column(DateTime)
	content_type = Column(SmallInteger)
	content = Column(Text)
	src_url = Column(String(1024))

	def __repr__(self):
		return '------ Memory ------\n' \
		       'id: {}\n' \
		       'mid: {}\n' \
		       'created_at: {}\n' \
		       'content_type: {}\n' \
		       'content: {}\n' \
		       'src_url: {}\n' \
			.format(self.id,
		            self.mid,
		            self.created_at,
		            self.content_type,
		            self.content,
		            self.src_url)

print("Module {} is loaded...".format(__file__))
