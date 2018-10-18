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
	path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update')
]
