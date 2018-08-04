# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# we will use the reverse() method that allows you to build URLs by their name and passing optional parameters.
from django.db.models import CharField
from django.urls import reverse

# Create your manager here.
class MomentManager(models.Manager):
	def get_pic_moment(self):
		return super(MomentManager, self).get_queryset().filter(content_type=3)

# Create your models here.
class PeekabooCollection(models.Model):

	COLLECTION_TYPE =  (
		(1, 'Collection'),
		(2, 'Text'),
		(3, 'Picture'),
		(4, 'Video'),
	)

	# The convention in Django is to add a get_absolute_url() method to the model that returns the canonical URL of the object.
	def get_absolute_url(self):
		# reverse need to first have url pattern in urls.py named
		return reverse('timehutBlog:collection_detail', args=[self.id])

	# null 是针对数据库而言，如果
	# null = True, 表示数据库的该字段可以为空。
	# blank 是针对表单的
	# blank = True, 表示你的表单填写该字段的时候可以不填
	id = models.CharField(primary_key=True, max_length=32)
	baby_id = models.CharField(max_length=32, blank=True, null=True)
	created_at = models.IntegerField(blank=True, null=True)
	updated_at = models.IntegerField(blank=True, null=True)
	months = models.IntegerField(blank=True, null=True)
	days = models.IntegerField(blank=True, null=True)
	content_type = models.SmallIntegerField(blank=True, null=True)
	caption = models.TextField(blank=True, null=True)
	'''
		# auto_now_add here, the date will be saved automatically when creating an object
		created = models.DateTimeField(auto_now_add=True)

		# auto_now here, the date will be updated automatically when saving an object.
		updated = models.DateTimeField(auto_now=True)

		# unique_for_date parameter to this field so we can build URLs
		# for posts using the date and slug of the post. Django will prevent from
		# multiple posts having the same slug for the same date
		slug = models.SlugField(max_length=250, unique_for_date='created_at')
	'''

	class Meta:
		# managed = False
		# managed＝True则告诉django可以对数据库进行操作
		managed = True
		db_table = 'peekaboo_collection'
		ordering = ('-created_at',)

	# 修改admin后台的显示
	# def __str__(self):
	# 	return f"{self.baby_id} - {self.id}"


class PeekabooMoment(models.Model):
	MOMENT_TYPE =  (
		(1, 'Text'),
		(2, 'Rich_text'),
		(3, 'Picture'),
		(4, 'Video'),
	)

	id = models.CharField(primary_key=True, max_length=32)
	event = models.ForeignKey(PeekabooCollection, on_delete=models.DO_NOTHING,
	                             related_name='event_id', blank=True, null=True)
	baby_id = models.CharField(max_length=32, blank=True, null=True)
	created_at = models.IntegerField(blank=True, null=True)
	updated_at = models.IntegerField(blank=True, null=True)
	content_type = models.SmallIntegerField(blank=True, null=True)
	content = models.TextField(blank=True, null=True)
	src_url = models.CharField(max_length=512, blank=True, null=True)
	months = models.IntegerField(blank=True, null=True)
	days = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'peekaboo_moment'
		ordering = ('-created_at',)

	# def __str__(self):
	# 	return f"{self.baby_id} - {self.id} - {self.event_id}"

	# The default manager
	objects = models.Manager()
	# Our custom manager
	# In Shell: Moment.getPictureContent.get_pic_moment()
	getPictureContent = MomentManager()
