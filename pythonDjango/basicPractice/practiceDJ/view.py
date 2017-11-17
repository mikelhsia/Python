# from django.http import HttpResponse
#
# def sayHelloWorld(request):
# 	return HttpResponse("Hello World!")

from django.shortcuts import render

# Django 模板查找机制： Django 查找模板的过程是在每个 app 的 templates 文件夹中找
# （而不只是当前 app 中的代码只在当前的 app 的 templates 文件夹中找）。各个 app 的
# templates 形成一个文件夹列表，Django 遍历这个列表，一个个文件夹进行查找，
# 当在某一个文件夹找到的时候就停止，所有的都遍历完了还找不到指定的模板的时候就是
# Template Not Found （过程类似于Python找包）。这样设计有利当然也有弊，有利是的
# 地方是一个app可以用另一个app的模板文件，弊是有可能会找错了。所以我们使用的时候在
# templates 中建立一个 app 同名的文件夹，这样就好了。
#
# 这就需要把每个app中的 templates 文件夹中再建一个 app 的名称，仅和该app相关的模板放在 app/templates/app/ 目录下面，

# 我们这里使用 render 来替代之前使用的 HttpResponse。render 还使用了一个字典 context 作为参数。
# context 字典中元素的键值 "hello" 对应了模板中的变量 "{{ hello }}"。
def sayHelloWorld(request):
    context = {}
    context['hello'] = "Hello World!"
    context['TutorialList'] = {"HTML", "CSS", "jQuery", "Python", "Django"}
    return render(request, 'templates_tutorial.html', context)


def sayHelloWorldBase(request):
    return render(request, 'helloBase.html')

def tryBootstrapsJquery(request):
    return render(request, 'home.html')