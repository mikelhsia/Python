from sqlalchemy import Column, String, Integer, DateTime, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import enum
class CollectionEnum(enum.Enum):
	collection = 1
	text = 2
	picture = 3
	video = 4

class MomentEnum(enum.Enum):
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
	content_type = Column(SmallInteger)
	caption = Column(Text)

	def __repr__(self):
		return '---- Collection ----\n' \
		       'id: {}\n' \
		       'baby_id: {}\n' \
		       'created_at: {}\n' \
		       'months: {} \n' \
		       'days: {} \n' \
		       'content_type: {}\n' \
		       'caption: {} \n' \
		       '--------------------'\
			.format(self.id,
		         self.baby_id,
		         self.created_at,
		         self.months,
		         self.days,
		         self.content_type,
		         self.caption)



class Moment(base):
	__tablename__ = 'peekaboo_moment'

	id = Column(String(32), primary_key=True)
	event_id = Column(String(32), ForeignKey('{}.id'.format(Collection.__tablename__))) 
	collection = relationship("Collection", backref=__tablename__)
	baby_id = Column(String(32))
	created_at = Column(DateTime)
	content_type = Column(SmallInteger)
	content = Column(Text)
	src_url = Column(String(512))
	months = Column(Integer)
	days = Column(Integer)

	def __repr__(self):
		return '------ Moment ------\n' \
		       'id: {}\n' \
		       'event_id: {}\n' \
		       'baby_id: {}\n' \
		       'created_at: {}\n' \
		       'content_type: {}\n' \
		       'content: {}\n' \
		       'src_url: {}\n' \
		       'months: {}\n' \
		       'days: {}\n' \
			.format(self.id,
		            self.event_id,
                    self.baby_id,
		            self.created_at,
		            self.content_type,
		            self.content,
		            self.src_url,
		            self.months,
		            self.days)

print("Module {} is loaded...".format(__file__))
