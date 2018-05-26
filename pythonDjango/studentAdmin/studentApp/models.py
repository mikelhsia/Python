from django.db import models

# Create your models here.

class Classes(models.Model):
	'''
	Classes table
	'''
	title = models.CharField(max_length=32)
	a     = models.ManyToManyField('Teachers')



class Teachers(models.Model):
	'''
	Teachers table
	'''
	name = models.CharField(max_length=32)


class Students(models.Model):
	username = models.CharField(max_length=32)
	age = models.IntegerField()
	gender = models.BooleanField()
	cs = models.ForeignKey(Classes, on_delete=models.CASCADE)


# To migrate tables:
# Run python3 manage.py makemigrations
# Run python3 manage.py migrate