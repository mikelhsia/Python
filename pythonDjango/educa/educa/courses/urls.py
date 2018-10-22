"""educa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, 
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
	path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
	path('create/', views.CourseCreateView.as_view(), name='course_create'),
	path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
	path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
	path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
	path('module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
	path('module/<int:module_id/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
	path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
	path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
	path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
	path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
]
