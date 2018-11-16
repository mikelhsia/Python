from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject, Course
from .serializers import SubjectSerializer

from rest_framework.authentication import BasicAuthentication

from rest_framework.permissions import IsAuthenticated

# Creating view sets and routers
from rest_framework import viewsets
from .serializers import CourseSerializer

# Adding additional actions to view sets
from rest_framework.decorators import action

from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer

class SubjectListView(generics.ListAPIView):
	'''
	queryset is the base QuerySet to use to retrieve objects
	serializer_class is the class to serialize objects
	'''
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer


class CourseEnrollView(APIView):
	# User will be identified by the credentials set in the Authorization header of the HTTP request
	authentication_classes = (BasicAuthentication, )
	# This will prevent anonymous users from accessing the view.
	permission_classes = (IsAuthenticated, )

	def post(self, request, pk, format=None):
		'''
		We create a post method for POST action. No other HTTP method will be allowed for this view.
		Also add the current user to the students many-to-many relationship of the Course object
		and return a successful response.
		:param request:
		:param pk:
		:param format:
		:return:
		'''
		course = get_object_or_404(Course, pk=pk)
		course.students.add(request.user)
		return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
	'''
	ReadOnlyModelViewSet: provides the read-only actions list() and retrieve() to both list objects or retrieve single object
	'''
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

	authentication_classes = (BasicAuthentication, )
	permission_classes = (IsAuthenticated, )

	@action(detail=True, methods=['post'])
	def enroll(self, request, *args, **kwargs):
		'''
		action decorator - detail - extra actions may be intended for either a single object, or an entire collection.
		method speficy only post is allowed
		We use self.get_object() to retrieve the Course object
		:param request:
		:param args:
		:param kwargs:
		:return:
		'''
		course = self.get_object()
		course.students.add(request.user)
		return Response({'enrolled': True})

	@action(detail=False, methods=['get'],
	        serializer_class=CourseWithContentsSerializer,
	        authentication_classes=[BasicAuthentication],
	        permission_classes=[IsAuthenticated, IsEnrolled])
	def contents(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)