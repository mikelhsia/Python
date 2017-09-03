#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
本文主要介绍python中调用REST
API的几种方式，下面是python中会用到的库。
- urllib2
- httplib2
- pycurl
- requests
============================================================
1. urllib2
- Sample1
======
import urllib2, urllib

github_url = 'https://api.github.com/user/repos'
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, github_url, 'user', '***')
auth = urllib2.HTTPBasicAuthHandler(password_manager)  # create an authentication handler
opener = urllib2.build_opener(auth)  # create an opener with the authentication handler
urllib2.install_opener(opener)  # install the opener...
request = urllib2.Request(github_url, urllib.urlencode(
	{'name': 'Test repo', 'description': 'Some test repository'}))  # Manual encoding required
handler = urllib2.urlopen(request)
print(handler.read())

- Sample2
======
import urllib2

url = 'http://ems.vip.ebay.com/removeSIforcloud.cgi?ip=' + ip
req = urllib2.Request(url)
req.add_header('IAF', abc.token_authiaas)
try:
	resp = urllib2.urlopen(req)
except urllib2.HTTPError, error:
	print("Cannot remove service instance!", error)
	sys.exit(1)
response = resp.read()
print(response)

- Sample3
======
import urllib2, urllib, base64

url = "https://reparo.stratus.ebay.com/reparo/bootstrap/registerasset/" + rackid + "/" + asset
data = urllib.urlencode({
	'reservedResource': 'RR-Hadoop',
	'resourceCapability': 'Production',
	'movetoironic': 'False',
	'output': 'json'
})
print("Bootstrap Asset jobs starting ..............")

base64string = base64.encodestring('%s:%s' % (user, passwd)).replace('\n', '')
request = urllib2.Request(url, data, headers={"Authorization": "Basic %s" % base64string})
response = urllib2.urlopen(request).read()
response_json = json.loads(response)
response_status = response_json['status']
status_code = response_status['statusCode']
status = response_status['status']
message = response_status['message']
print(status_code, status, message)

============================================================
2. httplib2
import urllib, httplib2

github_url = '
h = httplib2.Http(".cache")
h.add_credentials("user", "******", "
data = urllib.urlencode({"name": "test"})
resp, content = h.request(github_url, "POST", data)
print(content)

============================================================
3. pycurl
import pycurl, json

github_url = "
user_pwd = "user:*****"
data = json.dumps({"name": "test_repo", "description": "Some test repo"})
c = pycurl.Curl()
c.setopt(pycurl.URL, github_url)
c.setopt(pycurl.USERPWD, user_pwd)
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, data)
c.perform()

============================================================
4. requests
import requests, json

github_url = "
data = json.dumps({'name': 'test', 'description': 'some test repo'})
r = requests.post(github_url, data, auth=('user', '*****'))
print(r.json)
以上几种方式都可以调用API来执行动作，但requests这种方式代码最简洁，最清晰，建议采用。
'''

import requests, json, pprint

iexApiUrl = "https://api.iextrading.com/1.0/stock/aapl/news"
# data = json.dumps({'name': 'test', 'description': 'some test repo'})
# r = requests.post(github_url, data, auth=('user', '*****'))
g = requests.get(iexApiUrl)

aapl = json.loads(g.content)
# print(aapl['symbol'])
print(json.dumps(aapl, indent=4, sort_keys=True))

