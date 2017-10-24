from django.db import models

# Create your models here.
# 以下的类名代表了数据库表名，且继承了models.Model，类里面的字段代表数据表中的字段(name)，
# 数据类型则由CharField（相当于varchar）、DateField（相当于datetime）， max_length 参数限定长度。
class Test(models.Model):
	username = models.CharField('username', max_length=32)
	password = models.CharField('password', max_length=32)

	# 发现所有的文章都是叫 Article object，这样肯定不好，
	# 比如我们要修改，如何知道要修改哪个呢？
	# 我们修改一下 blog 中的models.py
	def __str__(self):
		return self.username

# $ python manage.py migrate   # 创建表结构
# $ python manage.py makemigrations TestModel  # 让 Django 知道我们在我们的模型有一些变更
# $ python manage.py migrate TestModel   # 创建表结构

class Contact(models.Model):
	name = models.CharField('name', max_length=200)
	age = models.IntegerField('age', default=0)
	email = models.EmailField('email')

	def __str__(self):
		return self.name


# Tag 以 Contact 为外部键。一个 Contact 可以对应多个 Tag
class Tag(models.Model):
	contact = models.ForeignKey(Contact)
	name = models.CharField('name', max_length=50)

	def __unicode__(self):
		return self.name

# $ python manage.py makemigrations TestModel  # 让 Django 知道我们在我们的模型有一些变更
# $ python manage.py migrate TestModel   # 创建表结构