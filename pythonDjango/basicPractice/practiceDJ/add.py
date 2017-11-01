from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse  # django 1.4.x - django 1.10.x
from django.urls import reverse  # new in django 1.10.x

def index(request):
	return render(request, "add.html")

def old_add_redirect(request, a, b):
	# return HttpResponseRedirect(reverse('add', args=(a, b)))
	return HttpResponseRedirect(reverse('add3', args=(a, b)))

def add3(request, a, b):
	return HttpResponse(str(int(a)+int(b)))
