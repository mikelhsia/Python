from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course
# Create your views here.
class StudentRegistrationView(CreateView):
	'''
	Using CreateView that provides the functionality for creating model objects
	'''
	template_name = 'students/student/registration.html'
	# The form for creating objects, which has to be a ModelForm. We use Django's UserCreationForm
	# as registration form to create User object
	form_class = UserCreationForm
	success_url = reverse_lazy('student_course_list')

	def form_valid(self, form):
		result = super(StudentRegistrationView, self).form_valid(form)

		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password'])
		login(self.request, user)

		return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
	course = None
	form_class = CourseEnrollForm

	def form_valid(self, form):
		self.course = form.cleaned_data['course']
		self.course.students.add(self.request.user)
		return super(StudentEnrollCourseView, self).form_valid(form)

	def get_success_url(self):
		'''
		This method is equivalent to the success_url attribute
		:return:
		'''
		return reverse_lazy('students:student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
	model = Course
	template_name = 'students/course/list.html'

	def get_queryset(self):
		qs = super(StudentCourseListView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
	model = Course
	template_name = 'students/course/detail.html'

	def get_queryset(self):
		qs = super(StudentCourseDetailView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])

	def get_context_data(self, **kwargs):
		context = super(StudentCourseDetailView, self).get_context_data(**kwargs)

		# Get course object
		course = self.get_object()

		if 'module_id' in self.kwargs:
			# get current module
			context['module'] = course.modules.get(id=self.kwargs['module_id'])
		else:
			# get first module
			context['module'] = course.modules.all()[0]

		return context