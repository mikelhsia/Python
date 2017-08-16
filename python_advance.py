#!/usr/local/bin/python
# -*- coding: UTF-8 -*-


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
print "---------------------"
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
