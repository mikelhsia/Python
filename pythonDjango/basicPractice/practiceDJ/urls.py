"""practiceDJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import view, testdb, search, searchPost, add

from django.conf import settings
from django.conf.urls.static import static

# Django url() 可以接收四个参数，分别是两个必选参数：regex、view 和两个可选参数：kwargs、name，接下来详细介绍这四个参数。
#  - regex: 正则表达式，与之匹配的 URL 会执行对应的第二个参数 view。
#  - view: 用于执行与正则表达式匹配的 URL 请求。
#  - kwargs: 视图使用的字典类型的参数。
#  - name: 用来反向获取 URL。
urlpatterns = [
    # name 可以用于在 templates, models, views ……中得到对应的网址，相当于“给网址取了个名字”，
    # 只要这个名字不变，网址变了也能通过名字获取到。
	url(r'^search-post', searchPost.search_post),
	url(r'^search-form', search.searchForm, name='searchForm'),
	url(r'^search', search.search),
	url(r'^helloBase', view.sayHelloWorldBase, name='base'),
	url(r'^hello', view.sayHelloWorld),
	url(r'^testdb$', testdb.testdb),
	url(r'^add/$', add.index, name='add'),
	url(r'^add/(\d+)/(\d+)/$', add.old_add_redirect, name='add2'),
	url(r'^new_add/(\d+)/(\d+)/$', add.add3, name='add3'),
	url(r'^admin/', admin.site.urls),
]
