from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your manager here.
class MomentManager(models.Manager):
	def get_pic_moment(self):
		return super(MomentManager, self).get_queryset().filter(content_type=3)

# Create your models here.
class Collection(models.Model):
	COLLECTION_TYPE =  (
		(1, 'Collection'),
 		(2, 'Text'),
 		(3, 'Picture'),
 		(4, 'Video'),
	)

	collection_id = models.CharField(max_length=32)
	baby_id = models.CharField(max_length=32)
	created_at = models.IntegerField()
	updated_at = models.IntegerField()
	months = models.IntegerField()
	days = models.IntegerField()
	content_type = models.PositiveSmallIntegerField()
	# content_type = models.CharField(max_length=24, choice=COLLECTION_TYPE)
	caption = models.TextField()
	
	# auto_now_add here, the date will be saved automatically when creating an object
	# created = models.DateTimeField(auto_now_add=True)

	# auto_now here, the date will be updated automatically when saving an object.
	# updated = models.DateTimeField(auto_now=True)

	# unique_for_date parameter to this field so we can build URLs
	# for posts using the date and slug of the post. Django will prevent from
	# multiple posts having the same slug for the same date
	# slug = models.SlugField(max_length=250, unique_for_date='created_at')
	slug = models.SlugField(max_length=250)


	# The class Meta inside the model contains metadata. Telling Django to sort results by "created_at" field
	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f"{self.baby_id} - {self.collection_id}"


class Moment(models.Model):
	MOMENT_TYPE =  (
		(1, 'Text'),
 		(2, 'Rich_text'),
 		(3, 'Picture'),
 		(4, 'Video'),
	)

	moment_id = models.CharField(max_length=32)
	event_id = models.ForeignKey(Collection, related_name='event_id', on_delete='PROTECT')
	baby_id = models.CharField(max_length=32)
	created_at = models.IntegerField()
	updated_at = models.IntegerField()
	content_type = models.PositiveSmallIntegerField()
	content = models.TextField()
	src_url = models.CharField(max_length=512)
	months = models.IntegerField()
	days = models.IntegerField()
	slug = models.SlugField(max_length=250)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f"{self.baby_id} - {self.moment_id} - {self.event_id}"

	# The default manager
	objects = models.Manager()
	# Our custom manager
	# In Shell: Moment.getPictureContent.get_pic_moment()
	getPictureContent = MomentManager()