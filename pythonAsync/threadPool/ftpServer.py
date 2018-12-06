from socket import *
from concurrent.futures import ProcessPoolExecutor
import os


server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8080))
server.listen(5)


def talk(conn, client_addr):
	print(f'PID: {os.getpid()}')
	while True:
		try:
			msg = conn.recv(1024)
			if not msg:
				break
			conn.send(msg.upper())

		except Exception:
			break


if __name__ == '__main__':
	p = ProcessPoolExecutor(5)
	while True:
		conn, client_addr = server.accept()
		p.submit(talk, conn, client_addr)