from rest_framework import serializers
from ..models import Subject, Course, Module, Content

class SubjectSerializer(serializers.ModelSerializer):
	'''
	This is the serializer for the Subjet model
	META model sepcify the model to serialize and fields to be serialized
	User serializer.data to retrieve serialized data
	1. JSONParser to serialize byte data
	2. JSONRenderer to parse the data into byte data
	'''
	class Meta:
		model = Subject
		fields = ('id', 'title', 'slug')

class ModuleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Module
		fields = ('order', 'title', 'description')

class CourseSerializer(serializers.ModelSerializer):
	'''
	We want to include more information about each module in the course object
	So we need to serialize Module objects and next them inside CourseSerializer
	'''

	# We add the modules attribute to CourseSerializer,
	# and set many=True to indicate that we are serializing multiple objects
	# and set read_only to indiates that this field is read-only and should not be included in any input
	modules = ModuleSerializer(many=True, read_only=True)

	class Meta:
		model = Course
		fields = ('id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules')

class ItemRelatedField(serializers.RelatedField):
	'''
	We define a custom field by subclassing the RelatedField serializer
	overriding the to_representation() method
	'''
	def to_representation(self, value):
		return value.render()


class ContentSerializer(serializers.ModelSerializer):
	'''
	Use custom field for the item generic foreign key
	'''
	item = ItemRelatedField(read_only=True)

	class Meta:
		model = Content
		fields = ('order', 'item')


class ModuleWithContentsSerializer(serializers.ModelSerializer):
	contents = ContentSerializer(many=True)

	class Meta:
		model = Module
		fields = {'order', 'title', 'description', 'contents'}


class CourseWithContentsSerializer(serializers.ModelSerializer):
	modules = ModuleWithContentsSerializer

	class Meta:
		model = Course
		fields = {'id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules'}
