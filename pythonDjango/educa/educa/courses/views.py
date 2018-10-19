from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course

# Using maxins for class-based views
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content
# LoginRequiredMixin:   Repllicates the login_required decorator's functionality
# PermissionRequiredMixin:  Grants access to the view to users that have a specific permission.
#                           Remember that superusers automatically have all permissions

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
# TemplateResponseMixin: rendering templates and returning an HTTP response. It requires a template_name to be rendered
#                        and provides render_to_response() method to pass it a context and render the template
# View: The vasic class-based view from Django
from .forms import ModuleFormSet

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



class CourseModuleUpdateView(TemplateResponseMixin, View):
	'''
	CourseModuleUpdateView handles the formset to add, update, and delete modules for a specific course
	'''
	template_name = 'courses/manage/module/formset.html'
	course = None

	def get_formset(self, data=None):
		'''
		To avoid repeating the code to build the formset.
		:param data:
		:return:
		'''
		return ModuleFormSet(instance=self.course, data=data)

	def dispatch(self, request, pk):
		'''
		This method is provided by the View class. It takse an HTTP request and it's parameters and attempts
		to delegate to a lowercase method that matches the HTTP method used. For ex:
		A GET request is delegated to the get() method and a POST request to a post() method
		:param request:
		:param pk:
		:return:
		'''
		self.course = get_object_or_404(Course, id=pk, owner=request.user)
		return super(CourseModuleUpdateView, self).dispatch(request, pk)

	def get(self, request, *args, **kwargs):
		'''
		Executed for GET request
		:param request:
		:param args:
		:param kwargs:
		:return:
		'''
		formset = self.get_formset()
		return self.render_to_response({'course': self.course, 'formset': formset})

	def post(self, request, *args, **kwargs):
		'''
		Executed for POST request we perform the following actions:
		1. Build a ModuleFormSet instance using the submitted data
		2. Execute the is_valid() to validate all of its forms
		3. Save() and redirect to the template
		:param request:
		:param args:
		:param kwargs:
		:return:
		'''
		formset = self.get_formset(data=request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('courses:manage_course_list')
		return self.render_to_response({'course': self.course, 'formset': formset})


def ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        '''
         Here, we check that the given model name is one of the four content models: text, video, image, or file
        '''
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)

        return None

    def get_form(self, model, *args, **kwargs):
        '''
        We build a dynamic form using the modelform_factory() function of the form's framework.
        '''
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        '''
        It receives the following URL parameters and stores the corresponding module, model, and content object as class attributes:
        - module_id: The id for the module that the content is/will be associated with.
        - model_name: The model name of the content to create/update.
        - id: The id of the object that is being updated. It's None to create new objects.
        '''
        self.module = get_object_or_404(Module, id=module_id, course__owener=request,user)
        self.model = self.get_model(model_name)

        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})


    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
                return redirect('module_content_list', self.module.id)

            return self.render_to_response({'form': form, 'object': self.obj)}
