# @classmethod and @staticmethod


# 第一步：代码从第一行开始执行 class 命令，此时会创建一个类 A 对象（没错，类也是对象，一切皆对象嘛）
# 同时初始化类里面的属性和方法，记住，此刻实例对象还没创建出来。
# 第二、三步：接着执行 a=A()，系统自动调用类的构造器，构造出实例对象 a
# 第四步：接着调用 a.m1(1) ，m1 是实例方法，内部会自动把实例对象传递给 self 参数进行绑定，也就是说， self 和 a 指向的都是同一个实例对象。
# 第五步：调用A.m2(1)时，python内部隐式地把类对象传递给 cls 参数，cls 和 A 都指向类对象。
class A(object):
	def m1(self, n):
		print("self: ", self)

	@classmethod
	def m2(cls, n):
		print("cls: ", cls)

	@staticmethod
	def m3(n):
		pass

a = A()
a.m1(1)		# self: .....
A.m2(1)		# cls: ......
A.m3(1)

# A.m1是一个还没有绑定实例对象的方法，对于未绑定方法，调用 A.m1 时必须显示地传入一个实例对象进去，
# 而a.m1是已经绑定了实例的方法，python隐式地把对象传递给了self参数，所以不再手动传递参数，这是调用实例方法的过程。


# m2是类方法，不管是 A.m2 还是 a.m2，都是已经自动绑定了类对象A的方法，对于后者，因为python可以通过实例对象a找到它所属的类是A，
# 找到A之后自动绑定到 cls。这使得我们可以在实例方法中通过使用 self.m2()这种方式来调用类方法和静态方法。


# m3是类里面的一个静态方法，跟普通函数没什么区别，与类和实例都没有所谓的绑定关系，它只不过是碰巧存在类中的一个函数而已。
# 不论是通过类还是实例都可以引用该方法。


########################################################################
# 如果在方法中不需要访问任何实例方法和属性，纯粹地通过传入参数并返回数据的功能性方法，那么它就适合用静态方法来定义，
# 它节省了实例化对象的开销成本，往往这种方法放在类外面的模块层作为一个函数存在也是没问题的，而放在类中，仅为这个类服务。
########################################################################




# 类方法的使用场景有：
# 作为工厂方法创建实例对象，例如内置模块 datetime.date 类中就有大量使用类方法作为工厂方法，以此来创建date对象。

class date:
	def __new__(cls, year, month=None, day=None):
		self = object.__new__(cls)
		self._year = year
		self._month = month
		self._day = day
		return self

	@classmethod
	def fromtimestamp(cls, t):
		y, m, d, * = _time.localtime(t)
		return cls(y, m, d)

	@classmethod
	def today(cls):
        t = _time.time()
		return cls.fromtimestamp(t)
