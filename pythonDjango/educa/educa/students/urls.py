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

app_name = 'students'

urlpatterns = [
	path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
	path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
	path('courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
	path('course/<int:pk>', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
	path('course/<int:pk>/<int:module_id>', views.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
]
