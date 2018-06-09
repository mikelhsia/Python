from sqlalchemy import Column, String, Integer, DateTime, Text , Enum, ARRAY
from sqlalchemy.ext.declarative import declarative_base

__base = declarative_base()

class Collection(__base):
	__tablename__ = 'peekaboo_collection'

	id = Column(String(32), primary_key=True)
	baby_id = Column(Integer)
	created_at = Column(DateTime)
	months = Column(Integer)
	days = Column(Integer)
	memory_type = Column(Enum('collection', 'text'))
	memory_id_list = Column(ARRAY(Integer))
	caption = Column(Text)

class Memory(__base):
	__tablename__ = 'peekaboo_memory'

	id = Column(Integer, primary_key=True, autoincrement=True)
	cid = Column(String(32))
	content_type = Column(Enum('picture', 'text', 'video'))
	content = Column(Text)
	src_url = Column(String(1024))

print("Module {} is loaded...".format(__file__))
