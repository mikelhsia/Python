#!/usr/bin/python
# -*- coding: UTF-8 -*-

f = open('workfile','rw')
print f

# f.read(size)
f.read()
f.readline()
f.readlines()

f.write("This is a test\n")
f.seek(5) # Go to the 6th byte in the file
f.tell()
f.seek(-3,2) # Go to the 3rd byte before the end
f.tell()

f.close()

###################
# 用关键字 with 处理文件对象是个好习惯。它的先进之处在于文件用完后会自动关闭，
# 就算发生异常也没关系。它是 try-finally 块的简写:
with open('workfile','r') as f:
	read_data = f.read()
f.close()


# Python 提供了一个名为 pickle 的标准模块。这是一个令人赞叹的模块，几乎可以把任何 Python 对象 
#（甚至是一些 Python 代码段！）表达为为字符串，这一过程称之为封装 （ pickling ）。
# 从字符串表达出重新构造对象称之为拆封（ unpickling ）。
# 封装状态中的对象可以存储在文件或对象中，也可以通过网络在远程的机器之间传输。

# 如果你有一个对象 x ，一个以写模式打开的文件对象 f ，封装对象的最简单的方法只需要一行代码:
# pickle.dump(x, f)
# x = pickle.load(f)