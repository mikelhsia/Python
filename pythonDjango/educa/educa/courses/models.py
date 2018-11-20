from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# Create your models here.
class Subject(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title


class Course(models.Model):
	owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.PROTECT)
	subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.PROTECT)
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	overview = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	# Student many to many field
	students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

	class Meta:
		ordering = ('-created', )

	def __str__(self):
		return self.title


class Module(models.Model):
	course = models.ForeignKey(Course, related_name="modules", on_delete=models.PROTECT)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	# Customize field
	order = OrderField(blank=True, for_fields=['course'])

	class Meta:
		ordering = ['order']

	def __str__(self):
		return f'{self.order}. {self.title}'


class Content(models.Model):
	module = models.ForeignKey(Module, related_name='contents', on_delete=models.PROTECT)
	# content_type = models.ForeignKey(ContentType)
	content_type = models.ForeignKey(ContentType,
	                                 limit_choices_to={'model_in':('text', 'video', 'image', 'file')},
	                                 on_delete=models.PROTECT)
	object_id = models.PositiveIntegerField()
	# A GenericForeignKey field to the related object by combining the two previous fields
	item = GenericForeignKey('content_type', 'object_id')

	order = OrderField(blank=True, for_fields=['module'])

	class Meta:
		ordering = ['order']

'''
Abstract models: 
An abstract model is a base class in which you define fields you want to include in all child models. 
Django doesn't create any database table for abstract models. A database table is created for each 
child model, including the fields inherited from the abstract class and the ones defined in the child model.

Multi-table inheritance: 
In multi-table inheritance, each model corresponds to a database table. Django creates a 
OneToOneField field for the relationship in the child's model to its parent. 
To use multi-table inheritance, you have to subclass an existing model. Django will create a
database table for both the original model and the sub-model

Proxy models: 
Proxy models are used to change the behavior of a model, for example, including additional methods or 
different meta options. Both models operate on the database table of the original model.
'''
# We're using abstract models here
class ItemBase(models.Model):
	# We need different related_name for each sub_model. So %(class)s is a placeholder for the model class name
	owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.PROTECT)
	title = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.title

	def render(self):
		'''
		This method uses the render_to_string() for rendering a template and returning the rendered content as a string.
		Each kind of content is rendered using a template named after the content model
		We use self._meta.model_name to buil the appropriate template name for la.
		:return:
		'''
		return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})



class Text(ItemBase):
	content = models.TextField()

class File(ItemBase):
	file = models.FileField(upload_to='files')

class Image(ItemBase):
	image = models.ImageField(upload_to='images')

class video(ItemBase):
	url = models.URLField()
