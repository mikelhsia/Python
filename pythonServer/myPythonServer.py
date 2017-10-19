# File name: myPythonServer.py
#########
# Log:
# 2017.10.17 Refer website https://tinyurl.com/yb7v4pq7 to improve this script

import socket

# Init socket
# 4. 不同点
# 4.1 建立socket传递的地址域，及bind() 的地址结构稍有区别：
# socket(): 分别传递不同的域AF_INET和AF_UNIX
# bind(): 的地址结构分别为sockaddr_in（制定IP端口）和sockaddr_un（指定路径名）
# 4.2 AF_INET需经过多个协议层的编解码，消耗系统cpu，并且数据传输需要经过网卡，受到网卡带宽的限制。AF_UNIX数据到达内核缓冲区后，由内核根据指定路径名找到接收方socket对应的内核缓冲区，直接将数据拷贝过去，不经过协议层编解码，节省系统cpu，并且不经过网卡，因此不受网卡带宽的限制。
# 4.3 AF_UNIX的传输速率远远大于AF_INET
# 4.4 AF_INET不仅可以用作本机的跨进程通信，同样的可以用于不同机器之间的通信，其就是为了在不同机器之间进行网络互联传递数据而生。而AF_UNIX则只能用于本机内进程之间的通信。
# 5. 使用场景
# AF_UNIX由于其对系统cpu的较少消耗，不受限于网卡带宽，及高效的传递速率，本机通信则首选AF_UNIX域。
# 不用多说，AF_INET则用于跨机器之间的通信。
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8081

sk.bind((host,port))

sk.listen(5) # 开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。


def handle_client(content):
	lines = str(content).split('\n\r\t')
	methodLine = lines[0]
	data = lines[-1]

	print("HTTP Method is: {}".format(methodLine.split(" ")[0]))
	print("Data is: {}".format(data))

while True:
	conn, addr = sk.accept()
	print("链接地址：{}".format(addr))
	conn.send(bytes('欢迎访问菜鸟教程', 'utf-8'))
	handle_client(conn.recv(4096))
	# conn.close()