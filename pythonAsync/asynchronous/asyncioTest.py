'''
没有了yield 或 yield from，而是async/await
没有了自造的loop()，取而代之的是asyncio.get_event_loop()
无需自己在socket上做异步操作，不用显式地注册和注销事件，aiohttp库已经代劳
没有了显式的 Future 和 Task，asyncio已封装
更少量的代码，更优雅的设计
'''
import asyncio
import aiohttp


host = 'http://example.com'
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}

loop = asyncio.get_event_loop()


async def fetch(url):
	async with aiohttp.ClientSession(loop=loop) as session:
		async with session.get(url) as response:
			response = await response.read()
			return response


if __name__ == '__main__':
	import time
	start = time.time()

	tasks = [fetch(host+url) for url in urls_todo]
	loop.run_until_complete(asyncio.gather(*tasks))

	end = time.time()
	print(end - start)