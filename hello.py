#!/usr/bin/python
# -*- coding: UTF-8 -*-

####################################################################################
# Python CGI deployment
# http://www.runoob.com/python/python-cgi.html
####################################################################################

print "Content-type:text/html"
#第一行的输出内容"Content-type:text/html"发送到浏览器并告知浏览器显示的内容类型为"text/html"。
print                               # 空行，告诉服务器结束头部脚本
print '''
<html>
<head>
<meta charset="utf-8">
<title>Hello Word - 我的第一个 CGI 程序！</title>
</head>
<body>
<h2>Hello Word! 我是来自菜鸟教程的第一CGI程序</h2>
'''

print "<b>环境变量</b><br>";
print "<ul>"
for key in os.environ.keys():
    print "<li><span style='color:green'>%30s </span> : %s </li>" % (key,os.environ[key])
print "</ul>"


print '''</body>
</html>
'''