"""studentAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from studentApp.views import classes, students, teachers, ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('classes.html', classes.get_classes),
    path('add_classes.html', classes.add_classes),
    path('del_classes.html', classes.del_classes),
    path('edit_classes.html', classes.edit_classes),

	path('set_teachers.html', classes.set_teachers),

    path('students.html', students.get_students),
    path('add_students.html', students.add_students),
    path('del_students.html', students.del_students),
    path('edit_students.html', students.edit_students),

    path('teachers.html', teachers.get_teachers),
    path('add_teachers.html', teachers.add_teachers),
    path('del_teachers.html', teachers.del_teachers),
    path('edit_teachers.html', teachers.edit_teachers),

    path('ajax1.html', ajax.ajax1),
    path('ajax2.html', ajax.ajax2),
    path('ajax4.html', ajax.ajax4),
]
