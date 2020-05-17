#from requests import request
import requests
import os
import urllib3
import bs4

targets = ['https://www.worksheetfun.com/preschool-worksheets/', 'https://www.worksheetfun.com/kindergarten-worksheets/']



headers = {
	'authority': 'www.worksheetfun.com',
	'cache-control': 'max-age=0',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-fetch-site': 'same-origin',
	# 'sec-fetch-mode: navigate',
	# 'sec-fetch-user: ?1',
	# 'sec-fetch-dest: document',
	# 'accept-language: en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
	# 'cookie: __cfduid=daaea3dc57aac714e3dd54da268d5668e1589385065; __utmc=235003399; __utmz=235003399.1589385071.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=0690e4960885b1e4:T=1589385072:S=ALNI_MYwylgURwgP_Am1NNyL_Kn7_yQQ4w; __utmt=1; __utma=235003399.911958809.1589385071.1589385071.1589616265.2; __utmb=235003399.1.10.1589616266',
}

Count = 0
Current = 0

for target in targets:
	response = requests.get(target, headers=headers)
	s = str(response.content, encoding='utf-8')
	soup = bs4.BeautifulSoup(s, 'html.parser')
	links_to_pages = [x['href'] for x in soup.table('a')]

	# TODO & TODO url => url/page/2...
	for page_link in links_to_pages:
		response2 = requests.get(page_link, headers=headers)

		s2 = str(response2.content, encoding='utf-8')
		soup2 = bs4.BeautifulSoup(s2, 'html.parser')
		group_of_links = [x['href'] for x in soup2.find_all('a', class_='PinImage')]
		Count += len(group_of_links)

		for link in group_of_links:
			response3 = requests.get(link, headers=headers)
			s3 = str(response3.content, encoding='utf-8')
			soup3 = bs4.BeautifulSoup(s3, 'html.parser')

			# Only the first download link is needed
			download_links = [x['href'] for x in soup3.find_all('a', string='Download')]

			print(f'Processing {download_links}...')

			if len(download_links) < 1:
				continue

			for download_link in download_links:

				filepath, filename = os.path.split(download_link)

				if os.path.exists(f'Downloads/tmp/{filename}') and os.path.isfile(f'Downloads/tmp/{filename}'):
					print(f'File: {filename} existed ({Current}/{Count})')
					Current += 1
					continue

				req = requests.get(download_link, headers=headers)

				if req.status_code == 200:
					with open(f'Downloads/tmp/{filename}', 'wb') as fp:
						fp.write(req.content)
					print(f'File: {filename} has been downloaded ({Current}/{Count})')
				Current += 1

print(f'({Current}/{Count}) has been processed')