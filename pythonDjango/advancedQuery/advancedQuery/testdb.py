from django.http import HttpResponse
 
from blog.models import Author, Article, Tag

# 数据库操作
def testdb(request):
    return HttpResponse("<p>数据添加成功！</p>")