from django.db import models

# Create your models here.
# 以下的类名代表了数据库表名，且继承了models.Model，类里面的字段代表数据表中的字段(name)，
# 数据类型则由CharField（相当于varchar）、DateField（相当于datetime）， max_length 参数限定长度。
class Test(models.Model):
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)


# $ python manage.py migrate   # 创建表结构
# $ python manage.py makemigrations TestModel  # 让 Django 知道我们在我们的模型有一些变更
# $ python manage.py migrate TestModel   # 创建表结构