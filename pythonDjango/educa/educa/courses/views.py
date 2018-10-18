from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course

# Using maxins for class-based views
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
# LoginRequiredMixin:   Repllicates the login_required decorator's functionality
# PermissionRequiredMixin:  Grants access to the view to users that have a specific permission.
#                           Remember that superusers automatically have all permissions

# Create your views here.

'''
# Creating class-based views to create, edit, and delete courses
class ManageCourseListView(ListView):
	model = Course
	template_name = 'courses/manage/course/list.html'

	def get_queryset(self):
		qs = super(ManageCourseListView, self).get_queryset()
		return qs.filter(owner=self.request.user)
'''

# We will start creating a mixin class that includes a common behavior and use it for the courses' views
class OwnerMixin(object):
	'''
	This method is used by the views to get the base QuerySet. Our mixin will override this method to filter objects
	by the owner attribute to retrieve objects that belong to the current user
	'''
	def get_queryset(self):
		qs = super(OwnerMixin, self).get_queryset()
		return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
	'''
	form_valid() is executed when the submitted form is valid
	The default behavior of this method is saving the instance for modelforms and redirecting the user to success_url
	We override this to set the current user in the owner attribute, so we set the owner for an object automatically
	when it's saved
	'''
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
	'''
	The model used for QuerySets. Used by all views
	'''
	model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
	'''
	fields: The fields of the model to build the model form of the CreateView and UpdateView
	success_url: redirect url when form is saved
	'''
	fields = ['subject', 'title', 'slug', 'overview']
	success_url = reverse_lazy('courses:manage_course_list')
	template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
	'''
	Lists the courses created by the user
	The base view (ListView) needs to be placed at the end
	'''
	template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
	'''
	Uses a modelform to create a new course object. This uses the fields define in the OwnerCourseEditMixin
	'''
	permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
	'''
	Allows editing an existing Course object.
	'''
	template_name = 'courses/manage/course/form.html'
	permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
	'''
	Inherits from OwnerCourseMixin and teh generic DeleteView.
	Define success_url to redirect the user after the object is deleted.
	'''
	template_name = 'courses/manage/course/delete.html'
	success_url = reverse_lazy('courses:manage_course_list')
	permission_required = 'courses.delete_course'