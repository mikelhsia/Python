from django.shortcuts import render, redirect, HttpResponse
from studentApp import models

def ajax1(request):
	return render(request, 'ajax1.html')


def ajax2(request):
	u = request.GET.get('username')
	p = request.GET.get('password')
	return HttpResponse('Say I do!')

def ajax4(request):
	nid = request.GET.get('nid')
	msg = "Succeeded!"
	try:
		models.Students.objects.get(id=nid).delete()
	except Exception as e:
		msg = str(e)
	return HttpResponse(msg)