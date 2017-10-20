from practiceDJApp.models import Test
from django.http import HttpResponse

def testdb(request):
	# Getting Data from Data
	############################################3
	# Initialize
	response = ""
	response1 = ""

	test1 = Test(username='runoob', password='123123q')
	test1.save()

	# 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
	list = Test.objects.all()

	# filter相当于SQL中的WHERE，可设置条件过滤结果
	# response2 = Test.objects.filter(id=1)

	# 获取单个对象
	# response3 = Test.objects.get(id=1)

	# 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
	response4 = Test.objects.order_by('username')[0:2]

	# 数据排序
	response5 = Test.objects.order_by("id")

	# 上面的方法可以连锁使用
	response6 = Test.objects.filter(username="runoob").order_by("id")

	# Modify/Update data
	test2 = Test.objects.get(id=test1.id-1)
	test2.username = "runxxb"
	test2.save()

	# 另外一种方式
	# Test.objects.filter(id=1).update(name='Google')

	# 修改所有的列
	# Test.objects.all().update(username='runxxb')

	for var in list:
		response1 += var.username + "({}), ".format(var.id)

	response = response1

	if len(list) > 30:
		Test.objects.all().delete()
		return HttpResponse("<p>全部数据删除成功...</p>")

	return HttpResponse("<p>添加数据成功... {}</p>".format(response))
