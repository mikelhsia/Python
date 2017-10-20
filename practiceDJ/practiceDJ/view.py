# from django.http import HttpResponse
#
# def sayHelloWorld(request):
# 	return HttpResponse("Hello World!")

from django.shortcuts import render

# 我们这里使用 render 来替代之前使用的 HttpResponse。render 还使用了一个字典 context 作为参数。
# context 字典中元素的键值 "hello" 对应了模板中的变量 "{{ hello }}"。
def sayHelloWorld(request):
	context = {}
	context['hello'] = "Hello World!"
	return render(request, 'hello.html', context)


def sayHelloWorldBase(request):
	return render(request, 'helloBase.html')
