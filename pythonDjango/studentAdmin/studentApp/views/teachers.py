from django.shortcuts import render, redirect
from studentApp import models

# Create your views here.
def get_teachers(request):
	tch_list = models.Teachers.objects.all()
	return render(request, 'get_teachers.html', {'tch_list':tch_list})


def add_teachers(request):
	if request.method == 'GET':
		return render(request, 'add_teachers.html')
	elif request.method == 'POST':
		name = request.POST.get('name', '')
		models.Teachers.objects.create(name=name)
		return redirect('/teachers.html')


def del_teachers(request):
	nid = request.GET.get('nid', '')
	models.Teachers.objects.filter(id=nid).delete()
	return redirect('/teachers.html')


def edit_teachers(request):
	if request.method == 'GET':
		nid = request.GET.get('nid', '')
		obj = models.Teachers.objects.get(id=nid)
		return render(request, 'edit_teachers.html', {'obj':obj})
	elif request.method == 'POST':
		nid = request.POST.get('nid', '')
		name = request.POST.get('name', '')
		models.Teachers.objects.filter(id=nid).update(name=name)
		return redirect('/teachers.html')
