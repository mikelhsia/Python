#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name: myPythonServer.py 

import socket

# Init socket
sk = socket.socket()
host = socket.gethostname()
port = 8081

sk.bind((host,port))

sk.listen(5) # 开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。

while True:
	conn, addr = sk.accept()
	print "链接地址：", addr
	conn.send('欢迎访问菜鸟教程')
	conn.close()