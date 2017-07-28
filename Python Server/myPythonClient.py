#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name: myPythonClient.py 

import socket

sk = socket.socket()
host = socket.gethostname()
port = 8081

sk.connect((host,port))

print sk.recv(1024) # 接收TCP数据，数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。
sk.close
