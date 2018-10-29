from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm

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
		return reverse_lazy('student_course_detail', args=[self.course.id])