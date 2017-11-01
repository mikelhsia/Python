'''
@Date    : 2017-11-01
@Author  : Michael Hsia
@Link    : 
@Version : 0.0.1
'''
from __future__ import unicode_literals
 
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    qq = models.CharField(max_length=10)
    addr = models.TextField()
    email = models.EmailField()

    def my_property(self):
        return self.firstname + ' ' + self.lastname
        
    my_property.short_description = "Full name of the person"

    full_name = property(my_property)
 
    def __str__(self):
        return self.firstname
 
 
@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(u'文章标题', max_length=50)
    author = models.ForeignKey(Author)
    # author.short_description = "作者"
    content = models.TextField(u'文章内容')
    score = models.IntegerField(u'评分')  # 文章的打分
    tags = models.ManyToManyField('Tag')
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable = True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True, null=True)
 
    def __str__(self):
        return self.title
 
 
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name
