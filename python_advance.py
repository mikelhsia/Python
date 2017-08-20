#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

def print_breakline():
	print "---------------------"

########################################################################################
# 不定函数 -
# 什么时候使用它们？
#
# 这还真的要看你的需求而定。
# 最常见的用例是在写函数装饰器的时候（会在另一章里讨论）。
# 此外它也可以用来做猴子补丁(monkey patching)。猴子补丁的意思是在程序运行时(runtime)修改某些代码。
# 打个比方，你有一个类，里面有个叫get_info的函数会调用一个API并返回相应的数据。如果我们想测试它，
# 可以把API调用替换成一些测试数据。例如：
#   import someclass
#
#   def get_info(self, *args):
#       return "Test data"
#
#   someclass.get_info = get_info
########################################################################################
def test_var_args(f_arg, *argv):
	print "First normal arg:", f_arg
	for arg in argv:
		print "another arg through *argv:", arg


def test_var_key_args(f_arg, *args, **kwargs):
	print "First normal arg:", f_arg
	for key in kwargs:
		print "[%s] = \'%s\'" % (key, kwargs[key])

test_var_args('yasoob', 'python', 'eggs', 'test')
print_breakline()
test_var_key_args('first', name='yasoob', lang='python', food='eggs', func='test')


########################################################################################
# pdo - Python Debugger command
# python -m pdb python_advance.py
########################################################################################
# - h(elp) [command]
# Without argument, print the list of available commands. With a command as argument,
# print help about that command. help pdb displays the full documentation (the docstring of the pdb module).
# Since the command argument must be an identifier, help exec must be entered to get help on the ! command.
#
# - w(here)
# Print a stack trace, with the most recent frame at the bottom.
# An arrow indicates the current frame, which determines the context of most commands.
#
# - d(own) [count]
# Move the current frame count (default one) levels down in the stack trace (to a newer frame).
#
# - u(p) [count]
# Move the current frame count (default one) levels up in the stack trace (to an older frame).
#
# - b(reak) [([filename:]lineno | function) [, condition]]
# With a lineno argument, set a break there in the current file. With a function argument,
# set a break at the first executable statement within that function. The line number may be prefixed
# with a filename and a colon, to specify a breakpoint in another file (probably one that hasn’t been loaded yet).
# The file is searched on sys.path. Note that each breakpoint is assigned a number to which all the other
# breakpoint commands refer.
#
# If a second argument is present, it is an expression which must evaluate to true before the breakpoint is honored.
#
# Without argument, list all breaks, including for each breakpoint, the number of times that breakpoint has been hit,
# the current ignore count, and the associated condition if any.
#
# - tbreak [([filename:]lineno | function) [, condition]]
# Temporary breakpoint, which is removed automatically when it is first hit. The arguments are the same as for break.
#
# - cl(ear) [filename:lineno | bpnumber [bpnumber …]]
# With a filename:lineno argument, clear all the breakpoints at this line. With a space separated
# list of breakpoint numbers, clear those breakpoints. Without argument, clear all breaks (but first ask confirmation).
#
# - disable [bpnumber [bpnumber …]]
# Disable the breakpoints given as a space separated list of breakpoint numbers.
# Disabling a breakpoint means it cannot cause the program to stop execution, but unlike clearing a
# breakpoint, it remains in the list of breakpoints and can be (re-)enabled.
#
# - enable [bpnumber [bpnumber …]]
# Enable the breakpoints specified.
#
# ignore bpnumber [count]
# Set the ignore count for the given breakpoint number. If count is omitted, the ignore count is set to 0.
# A breakpoint becomes active when the ignore count is zero. When non-zero, the count is decremented each time
# the breakpoint is reached and the breakpoint is not disabled and any associated condition evaluates to true.
#
# condition bpnumber [condition]
# Set a new condition for the breakpoint, an expression which must evaluate to true before the breakpoint
# is honored. If condition is absent, any existing condition is removed; i.e., the breakpoint is made unconditional.
#
# commands [bpnumber]
# Specify a list of commands for breakpoint number bpnumber. The commands themselves appear
# on the following lines. Type a line containing just end to terminate the commands. An example:
#   (Pdb) commands 1
#   (com) p some_variable
#   (com) end
#   (Pdb)
# To remove all commands from a breakpoint, type commands and follow it immediately with end; that is, give no commands.
#
# With no bpnumber argument, commands refers to the last breakpoint set.
#
# You can use breakpoint commands to start your program up again. Simply use the continue
# command, or step, or any other command that resumes execution.
#
# Specifying any command resuming execution (currently continue, step, next, return,
# jump, quit and their abbreviations) terminates the command list (as if that command was
# immediately followed by end). This is because any time you resume execution (even with a
# simple next or step), you may encounter another breakpoint—which could have its own command
# list, leading to ambiguities about which list to execute.
#
# If you use the ‘silent’ command in the command list, the usual message about stopping at a
# breakpoint is not printed. This may be desirable for breakpoints that are to print a specific
# message and then continue. If none of the other commands print anything, you see no sign that
# the breakpoint was reached.
#
# s(tep)
# Execute the current line, stop at the first possible occasion (either in a function that is
# called or on the next line in the current function).
#
# n(ext)
# Continue execution until the next line in the current function is reached or it returns.
# (The difference between next and step is that step stops inside a called function, while next executes
# called functions at (nearly) full speed, only stopping at the next line in the current function.)
#
# unt(il) [lineno]
# Without argument, continue execution until the line with a number greater than the current one is reached.
#
# With a line number, continue execution until a line with a number greater or equal to that is reached.
# In both cases, also stop when the current frame returns.
#
# Changed in version 3.2: Allow giving an explicit line number.
#
# r(eturn)
# Continue execution until the current function returns.
#
# c(ont(inue))
# Continue execution, only stop when a breakpoint is encountered.
#
# j(ump) lineno
# Set the next line that will be executed. Only available in the bottom-most frame. This lets you
# jump back and execute code again, or jump forward to skip code that you don’t want to run.
#
# It should be noted that not all jumps are allowed – for instance it is not possible to jump into the
# middle of a for loop or out of a finally clause.
#
# l(ist) [first[, last]]
# List source code for the current file. Without arguments, list 11 lines around the current line or
# continue the previous listing. With . as argument, list 11 lines around the current line. With one
# argument, list 11 lines around at that line. With two arguments, list the given range; if the second
# argument is less than the first, it is interpreted as a count.
#
# The current line in the current frame is indicated by ->. If an exception is being debugged, the line
# where the exception was originally raised or propagated is indicated by >>, if it differs from the current line.
#
# New in version 3.2: The >> marker.
#
# ll | longlist
# List all source code for the current function or frame. Interesting lines are marked as for list.
#
# New in version 3.2.
#
# a(rgs)
# Print the argument list of the current function.
#
# p expression
# Evaluate the expression in the current context and print its value.
#
# Note print() can also be used, but is not a debugger command — this executes the Python print() function.
# pp expression
# Like the p command, except the value of the expression is pretty-printed using the pprint module.
#
# whatis expression
# Print the type of the expression.
#
# source expression
# Try to get source code for the given object and display it.
#
# New in version 3.2.
#
# display [expression]
# Display the value of the expression if it changed, each time execution stops in the current frame.
#
# Without expression, list all display expressions for the current frame.
#
# New in version 3.2.
#
# undisplay [expression]
# Do not display the expression any more in the current frame. Without expression, clear all display
# expressions for the current frame.
#
# New in version 3.2.
#
# interact
# Start an interactive interpreter (using the code module) whose global namespace contains all the
# (global and local) names found in the current scope.
#
# New in version 3.2.
#
# alias [name [command]]
# Create an alias called name that executes command. The command must not be enclosed in quotes.
# Replaceable parameters can be indicated by %1, %2, and so on, while %* is replaced by all the
# parameters. If no command is given, the current alias for name is shown. If no arguments are
# given, all aliases are listed.
#
# Aliases may be nested and can contain anything that can be legally typed at the pdb prompt.
# Note that internal pdb commands can be overridden by aliases. Such a command is then hidden
# until the alias is removed. Aliasing is recursively applied to the first word of the command
# line; all other words in the line are left alone.
#
# As an example, here are two useful aliases (especially when placed in the .pdbrc file):
#
# # Print instance variables (usage "pi classInst")
# alias pi for k in %1.__dict__.keys(): print("%1.",k,"=",%1.__dict__[k])
# # Print instance variables in self
# alias ps pi self
# unalias name
# Delete the specified alias.
#
# ! statement
# Execute the (one-line) statement in the context of the current stack frame. The exclamation
# point can be omitted unless the first word of the statement resembles a debugger command.
# To set a global variable, you can prefix the assignment command with a global statement on
# the same line, e.g.:
#   (Pdb) global list_options; list_options = ['-l']
#   (Pdb)
#   run [args …]
#   restart [args …]
# Restart the debugged Python program. If an argument is supplied, it is split with shlex and
# the result is used as the new sys.argv. History, breakpoints, actions and debugger options are
# preserved. restart is an alias for run.
#
# q(uit)
# Quit from the debugger. The program being executed is aborted.
########################################################################################

print_breakline()
my_string = "Yasoob"
my_iter = iter(my_string)
print next(my_iter)
print next(my_iter)
print next(my_iter)
print next(my_iter)
# Output: 'Y'


print_breakline()
items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))
print squared

def multiply(x):
	return (x*x)

def add(x):
	return (x+x)

funcs = [multiply, add]

for i in range(5):
	value = map(lambda x: x(i), funcs)
	print(list(value))
	# 译者注：上面print时，加了list转换，是为了python2/3的兼容性
	#        在python2中map直接返回列表，但在python3中返回迭代器
	#        因此为了兼容python3, 需要list转换一下


print_breakline()
number_list = range(-5, 5)
# 这个filter类似于一个for循环，但它是一个内置函数，并且更快
less_than_zero = filter(lambda x: x < 0, number_list)
print less_than_zero
# 译者注：上面print时，加了list转换，是为了python2/3的兼容性
#        在python2中filter直接返回列表，但在python3中返回迭代器
#        因此为了兼容python3, 需要list转换一下
# Output: [-5, -4, -3, -2, -1]


from functools import reduce
# 当需要对一个列表进行一些计算并返回结果时，Reduce 是个非常有用的函数
product = reduce( (lambda x, y: x * y), [1, 2, 3, 4] )
# Output: 24

print_breakline()
# set(集合)数据结构
# 它与列表(list)的行为类似，区别在于set不能包含重复的值。
# 这在很多情况下非常有用。例如你可能想检查列表中是否包含重复的元素，你有两个选择，第一个需要使用for循环
# 但还有一种更简单更优雅的解决方案，那就是使用集合(sets)

some_list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
duplicates = set([x for x in some_list if some_list.count(x) > 1])
print(duplicates)
# 重复
# 输出: set(['b', 'n'])

valid = set(['yellow', 'red', 'blue', 'green', 'black'])
input_set = set(['red', 'brown'])
print(input_set.intersection(valid))
# 交集
# 输出: set(['red'])

valid = set(['yellow', 'red', 'blue', 'green', 'black'])
input_set = set(['red', 'brown'])
print(input_set.difference(valid))
# 差集
# 输出: set(['brown'])


# 伪代码:
# 如果条件为真，返回真 否则返回假
#   condition_is_true if condition else condition_is_false
# 例子:
is_fat = True
state = "fat" if is_fat else "not fat"
print state

# 伪代码:
# (返回假，返回真)[真或假]
#   (if_test_is_false, if_test_is_true)[test]
# 例子:
fat = True
fitness = ("skinny", "fat")[fat]
print("Ali is ", fitness)
#输出: Ali is fat

print_breakline()
# 装饰器
# Decorator
##############################################
# Step 1: 一切皆对象
##############################################
def hi(name="yasoob"):
	return "hi " + name

print(hi())
# output: 'hi yasoob'

# 我们甚至可以将一个函数赋值给一个变量，比如
greet = hi
# 我们这里没有在使用小括号，因为我们并不是在调用hi函数
# 而是在将它放在greet变量里头。我们尝试运行下这个

print(greet())
# output: 'hi yasoob'

# 如果我们删掉旧的hi函数，看看会发生什么！
# del hi
# print(hi())
#outputs: NameError

print(greet())
#outputs: 'hi yasoob'


print_breakline()
##############################################
# Step 2 在函数中定义函数
##############################################
def hi(name="yasoob"):
	print("now you are inside the hi() function")

	def greet():
		return "now you are in the greet() function"

	def welcome():
		return "now you are in the welcome() function"

	print(greet())
	print(welcome())
	print("now you are back in the hi() function")

hi()
#output:now you are inside the hi() function
#       now you are in the greet() function
#       now you are in the welcome() function
#       now you are back in the hi() function

# 上面展示了无论何时你调用hi(), greet()和welcome()将会同时被调用。
# 然后greet()和welcome()函数在hi()函数之外是不能访问的，比如：

greet()
#outputs: NameError: name 'greet' is not defined

print_breakline()
##############################################
# Step 3 从函数中返回函数
##############################################
def hi(name="yasoob"):
	def greet():
		return "now you are in the greet() function"

	def welcome():
		return "now you are in the welcome() function"

	if name == "yasoob":
		return greet
	else:
		return welcome

a = hi()
print(a)
#outputs: <function greet at 0x7f2143c01500>
#上面清晰地展示了`a`现在指向到hi()函数中的greet()函数

#现在试试这个
print(a())
#outputs: now you are in the greet() function


print_breakline()
##############################################
# Step 4 将函数作为参数传给另一个函数
##############################################
def hi():
	return "hi yasoob!"

def doSomethingBeforeHi(func):
	print("I am doing some boring work before executing hi()")
	print(func())

doSomethingBeforeHi(hi)
# outputs:
# I am doing some boring work before executing hi()
# hi yasoob!

print_breakline()
##############################################
# Step 5 你的第一个装饰器
##############################################
def a_new_decorator(a_func):

	"""This is newDecorator"""
	def wrapTheFunction():
		"""This is wrapTheFunction"""
		print("I am doing some boring work before executing a_func()")
		a_func()
		print("I am doing some boring work after executing a_func()")

	return wrapTheFunction

def a_function_requiring_decoration():
	print("I am the function which needs some decoration to remove my foul smell")

a_function_requiring_decoration()
#outputs: "I am the function which needs some decoration to remove my foul smell"

a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
#now a_function_requiring_decoration is wrapped by wrapTheFunction()

a_function_requiring_decoration()
#outputs:I am doing some boring work before executing a_func()
#        I am the function which needs some decoration to remove my foul smell
#        I am doing some boring work after executing a_func()


print_breakline()
##############################################
@a_new_decorator
def a_function_requiring_decoration():
	"""Hey you! Decorate me!"""
	print("I am the function which needs some decoration to "
		"remove my foul smell")

a_function_requiring_decoration()
#outputs: I am doing some boring work before executing a_func()
#         I am the function which needs some decoration to remove my foul smell
#         I am doing some boring work after executing a_func()

#the @a_new_decorator is just a short way of saying:
# a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

print(a_function_requiring_decoration.__name__)
print(a_function_requiring_decoration.__doc__)
# Output: wrapTheFunction
# 这里的函数被warpTheFunction替代了。它重写了我们函数的名字和注释文档(docstring)


print_breakline()
##############################################
from functools import wraps
def a_new_decorator(a_func):
	"""This is newDecorator"""
	@wraps(a_func)
	def wrapTheFunction():
		"""This is wrapTheFunction"""
		print("I am doing some boring work before executing a_func()")
		a_func()
		print("I am doing some boring work after executing a_func()")
	return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
	"""Hey yo! Decorate me!"""
	print("I am the function which needs some decoration to "
		"remove my foul smell")

print(a_function_requiring_decoration.__name__)
print(a_function_requiring_decoration.__doc__)
# Output: a_function_requiring_decoration

print_breakline()
##############################################
# 注意：@wraps接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。
# 这可以让我们在装饰器里面访问在装饰之前的函数的属性。
def decorator_name(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if not can_run:
			return "Function will not run"
		return f(*args, **kwargs)
	return decorated

@decorator_name
def func():
	return("Function is running")

can_run = True
print(func())
# Output: Function is running

can_run = False
print(func())
# Output: Function will not run

##############################################
# Step 6 使用场景：授权
# 装饰器能有助于检查某个人是否被授权去使用一个web应用的端点(endpoint)。
# 它们被大量使用于Flask和Django web框架中。这里是一个例子来使用基于装饰器的授权：
##############################################
# def requires_auth(f):
# 	@wraps(f)
# 	def decorated(*args, **kwargs):
# 		auth = request.authorization
# 		if not auth or not check_auth(auth.username, auth.password):
# 			authenticate()
# 			return f(*args, **kwargs)
# 		return decorated

##############################################
# Step 7 使用场景：日志
# 日志是装饰器运用的另一个亮点。这是个例子：
##############################################
# def logit(func):
# 	@wraps(func)
# 	def with_logging(*args, **kwargs):
# 		print(func.__name__ + " was called")
# 		return func(*args, **kwargs)
# 	return with_logging
#
# @logit
# def addition_func(x):
# 	"""Do some math."""
# 	return x + x
#
#
# result = addition_func(4)
# Output: addition_func was called

##############################################
# Step 7.1 使用场景：日志
# 日志的例子，并创建一个包裹函数，能让我们指定一个用于输出的日志文件
##############################################
def logit(logfile='out.log'):
	def logging_decorator(func):
		@wraps(func)
		def wrapped_function(*args, **kwargs):
			log_string = func.__name__ + " was called"
			print(log_string)
			# 打开logfile，并写入内容
			with open(logfile, 'a') as opened_file:
				# 现在将日志打到指定的logfile
				opened_file.write(log_string + '\n')
			return func(*args, **kwargs)
		return wrapped_function
	return logging_decorator

@logit()
def myfunc1():
	pass

myfunc1()
# Output: myfunc1 was called
# 现在一个叫做 out.log 的文件出现了，里面的内容就是上面的字符串

@logit(logfile='func2.log')
def myfunc2():
	pass

myfunc2()
# Output: myfunc2 was called
# 现在一个叫做 func2.log 的文件出现了，里面的内容就是上面的字符串


##############################################
# Step 7.2 使用场景：日志
# 类也可以用来构建装饰器。那我们现在以一个类而不是一个函数的方式，来重新构建logit。
##############################################
class logit(object):
	def __init__(self, logfile='out.log'):
		self.logfile = logfile

	def __call__(self, func):
		@wraps(func)
		def wrapped_function(*args, **kwargs):
			log_string = func.__name__ + " was called"
			print(log_string)
			# 打开logfile并写入
			with open(self.logfile, 'a') as opened_file:
				# 现在将日志打到指定的文件
				opened_file.write(log_string + '\n')
			# 现在，发送一个通知
			self.notify()
			return func(*args, **kwargs)
		return wrapped_function

	def notify(self):
		# logit只打日志，不做别的
		pass

# 这个实现有一个附加优势，在于比嵌套函数的方式更加整洁，而且包裹一个函数还是使用跟以前一样的语法：

@logit()
def myfunc1():
	pass

# 现在，我们给logit创建子类，来添加email的功能(虽然email这个话题不会在这里展开)。
# 从现在起，@email_logit将会和@logit产生同样的效果，但是在打日志的基础上，还会多发送一封邮件给管理员。

class email_logit(logit):
	'''
	一个logit的实现版本，可以在函数调用时发送email给管理员
	'''
	def __init__(self, email='admin@myproject.com', *args, **kwargs):
		self.email = email
		super(logit, self).__init__(*args, **kwargs)

	def notify(self):
		# 发送一封email到self.email
		# 这里就不做实现了
		pass
