'''
attrs library to resolve the issue below:
1. 特点是初始化参数很多，每一个都需要self.xx = xx 这样往实例上赋值。我印象见过一个类有30多个参数，这个init方法下光是赋值就占了一屏多...
2，如果不定义__repr__方法，打印类对象的方式很不友好，
3. 对象比较，有时候需要判断2个对象是否相等甚至大小
4. 有些场景下希望对对象去重，可以添加__hash__:
5. 给类写一个to_dict、to_json或者as_dict这样的方法，把类里面的属性打包成一个字典返回。基本都是每个类都要写一遍它：
'''

import attr

@attr.s(hash = True)
class Product (object):
	id = attr.ib();
	author_id = attr.ib()
	brand_id = attr.ib()
	spu_id = attr.ib()
	title = attr.ib(repr=False, cmp=False, hash=False)
	item_id = attr.ib(repr=False, cmp=False, hash=False)
	n_comments = attr.ib(repr=False, cmp=False, hash=False)
	creation_time = attr.ib(repr=False, cmp=False, hash=False)
	update_time = attr.ib(repr=False, cmp=False, hash=False)
	source = attr.ib(default='', repr=False, cmp=False, hash=False)
	parent_id = attr.ib(default=0, repr=False, cmp=False, hash=False)
	ancestor_id = attr.ib(default=0, repr=False, cmp=False, hash=False)


'''
In : p1 = Product(1, 100001, 2003, 20, 1002393002, '这是一个测试商品1', 2000001, 100, None, 1)

In : p2 = Product(1, 100001, 2003, 20, 1002393002, '这是一个测试商品2', 2000001, 100, None, 2)

In : p3 = Product(3, 100001, 2003, 20, 1002393002, '这是一个测试商品3', 2000001, 100, None, 3)

In : p1
Out: Product(id=1, author_id=100001, brand_id=2003, spu_id=20)

In : p1 == p2
Out: True

In : p1 > p3
Out: False

In : {p1, p2, p3}
Out:
{Product(id=1, author_id=100001, brand_id=2003, spu_id=20),
 Product(id=3, author_id=100001, brand_id=2003, spu_id=20)}

In : attr.asdict(p1)
Out:
{'ancestor_id': 0,
 'author_id': 100001,
 'brand_id': 2003,
 'creation_time': 100,
 'id': 1,
 'item_id': '这是一个测试商品1',
 'n_comments': 2000001,
 'parent_id': 0,
 'source': 1,
 'spu_id': 20,
 'title': 1002393002,
 'update_time': None}

In : attr.asdict(p1, filter=lambda a, v: a.name in ('id', 'title', 'author_id'))
Out: {'author_id': 100001, 'id': 1, 'title': 1002393002}
'''

'''
字段类型验证
业务代码中经验会对对象属性的类型和内容验证，attrs也提供了验证支持。验证有2种方案：
'''
# 1. 装饰器
@attr.s
class C(object):
	x = attr.ib()

	@x.validator
	def check(self, attribute, value):
		if value > 42:
			raise ValueError("{} must be smaller or equal to 42".format(attribute))

# 2. 属性参数
def x_smaller_than_y(instance, attribute, value):
	if value >= instance.y:
		raise ValueError("'x' has to be smaller than 'y'!")

@attr.s
class C(object):
	x = attr.ib(validator=[attr.validators.instance_of(int), x_smaller_than_y])
	y = attr.ib()

'''
属性类型转化
Python不会检查传入的值的类型，类型错误很容易发生，attrs支持自动的类型转化
'''
@attr.s
class C(object):
	x = attr.ib(converter=int)


'''
dataclasses模块
在Python 3.7里面会添加一个新的模块 dataclasses ，它基于PEP 557，Python 3.6可以通过pip下载安装使用:
'''
from datetime import datetime
from dataclasses import dataclass, field


@dataclass(hash=True, order=True)
class Product(object):
	id: int
	author_id: int
	brand_id: int
	spu_id: int
	title: str = field(hash=False, repr=False, compare=False)
	item_id: int = field(hash=False, repr=False, compare=False)
	n_comments: int = field(hash=False, repr=False, compare=False)
	creation_time: datetime = field(default=None, repr=False, compare=False,hash=False)
	update_time: datetime = field(default=None, repr=False, compare=False, hash=False)
	source: str = field(default='', repr=False, compare=False, hash=False)
	parent_id: int = field(default=0, repr=False, compare=False, hash=False)
	ancestor_id: int = field(default=0, repr=False, compare=False, hash=False)