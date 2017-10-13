#!/usr/local/bin/python
# -*- coding:UTF-8 -*-

# Python 展现了“瑞士军刀”的哲学。 这可以通过它更大的包的高级和健壮的功能来得到最好的展现。 例如:

# xmlrpc.client 和 xmlrpc.server 模块让远程过程调用变得轻而易举。 尽管模块有这样的名字，用户无需拥有XML的知识或处理XML。
# email 包是一个管理邮件信息的库，包括MIME和其它基于RFC 2822的信息文档。 不同于实际发送和接收信息的 smtplib 和 poplib 模块， email 包包含一个构造或解析复杂消息结构（包括附件）及实现互联网编码和头协议的完整工具集。
# xml.dom 和 xml.sax 包为流行的信息交换格式提供了强大的支持。同样， csv 模块支持在通用数据库格式中直接读写。综合起来，这些模块和包大大简化了 Python 应用程序和其它工具之间的数据交换。
# 国际化由 gettext ， locale 和 codecs 包支持。

# os 模块提供了很多与操作系统交互的函数:
import os

# 针对日常的文件和目录管理任务，shutil 模块提供了一个易于使用的高级接口:
import shutil

# glob 模块提供了一个函数用于从目录通配符搜索中生成文件列表:
import glob

# 通用工具脚本经常调用命令行参数。这些命令行参数以链表形式存储于 sys 模块的 argv 变量。
# getopt 模块使用 Unix getopt() 函数处理 sys.argv 。
# 更多的复杂命令行处理由 argparse 模块提供。
# sys 还有 stdin ， stdout 和 stderr 属性，即使在 stdout 被重定向时，后者也可以用于显示警告和错误信息:
import sys

# re 模块为高级字符串处理提供了正则表达式工具。对于复杂的匹配和处理，正则表达式提供了简洁、优化的解决方案:
import re

# math 模块为浮点运算提供了对底层 C 函数库的访问:
import math

# random 提供了生成随机数的工具:
import re

# 其中最简单的两个是用于处理从 urls 接收的数据的 urllib2 以及用于发送电子邮件的 smtplib:
import urllib2
import smtplib

# datetime 模块为日期和时间处理同时提供了简单和复杂的方法。
# 支持日期和时间算法的同时，实现的重点放在更有效的处理和格式化输出。该模块还支持时区处理:
import datetime

# 以下模块直接支持通用的数据打包和压缩格式： zlib, gzip, bz2, zipfile 以及 tarfile:
import zlib

# 有些用户对了解解决同一问题的不同方法之间的性能差异很感兴趣。Python 提供了一个度量工具，为这些问题提供了直接答案。
# 例如，使用元组封装和拆封来交换元素看起来要比使用传统的方法要诱人的多。 timeit 证明了后者更快一些:
import timeit

# 开发高质量软件的方法之一是为每一个函数开发测试代码，并且在开发过程中经常进行测试。
# doctest 模块提供了一个工具，扫描模块并根据程序中内嵌的文档字符串执行测试。
# 测试构造如同简单的将它的输出结果剪切并粘贴到文档字符串中。
# 通过用户提供的例子，它发展了文档，允许 doctest 模块确认代码的结果是否与文档一致:
import doctest
# unittest 模块不像 doctest 模块那么容易使用，不过它可以在一个独立的文件里提供一个更全面的测试集:
import unittest

# repr 模块为大型的或深度嵌套的容器缩写显示提供了 repr() 函数的一个定制版本:
import repr

# pprint 模块给老手提供了一种解释器可读的方式深入控制内置和用户自定义对象的打印。
# 当输出超过一行的时候，“美化打印（pretty printer）”添加断行和标识符，使得数据结构显示的更清晰
import pprint

# textwrap 模块格式化文本段落以适应设定的屏宽:
import textwrap

# locale 模块按访问预定好的国家信息数据库。locale 的格式化函数属性集提供了一个直接方式以分组标示格式化数字:
import locale

# string 提供了一个灵活多变的模版类 Template ，使用它最终用户可以简单地进行编辑。这使用户可以在不进行改变的情况下定制他们的应用程序。
from string import Template


# struct 模块为使用变长的二进制记录格式提供了 pack() 和 unpack() 函数。 
# 下面的示例演示了在不使用 zipfile 模块的情况下如何迭代一个 ZIP 文件的头信息。 
# 压缩码 "H" 和 "I" 分别表示2和4字节无符号数字， "<" 表明它们都是标准大小并且按照 little-endian 字节排序。
import struct

# 线程是一个分离无顺序依赖关系任务的技术。在某些任务运行于后台的时候应用程序会变得迟缓，线程可以提升其速度。
# 一个有关的用途是在 I/O 的同时其它线程可以并行计算。
# 下面的代码显示了高级模块 threading 如何在主程序运行的同时运行任务
import threading, zipfile

# logging 模块提供了完整和灵活的日志系统。它最简单的用法是记录信息并发送到一个文件或 sys.stderr:
import logging

# 这个工作方式对大多数应用程序工作良好，但是偶尔会需要跟踪对象来做一些事。不幸的是，仅仅为跟踪它们创建引用也会使其长期存在。 
# weakref 模块提供了不用创建引用的跟踪对象工具，一旦对象不再存在，它自动从弱引用表上删除并触发回调。
# 典型的应用包括捕获难以构造的对象
import weakref, gc

# array 模块提供了一个类似列表的 array() 对象，它仅仅是存储数据，更为紧凑。
# 以下的示例演示了一个存储双字节无符号整数的数组（类型编码 "H" ）而非存储 16 字节 Python 整数对象的普通正规列表:
from array import array

# collections 模块提供了类似列表的 deque() 对象，它从左边添加（append）和弹出（pop）更快，但是在内部查询更慢。
# 这些对象更适用于队列实现和广度优先的树搜索:
from collection import deque

# 除了链表的替代实现，该库还提供了 bisect 这样的模块以操作存储链表
import bisect

# heapq 提供了基于正规链表的堆实现。最小的值总是保持在 0 点。这在希望循环访问最小元素但是不想执行完整堆排序的时候非常有用
from heapq import heapify, heappop, headpusho

# decimal 模块提供了一个 Decimal 数据类型用于浮点数计算。相比内置的二进制浮点数实现 float ，这个类型有助于
#  - 金融应用和其它需要精确十进制表达的场合，
#  - 控制精度，
#  - 控制舍入以适应法律或者规定要求，
#  - 确保十进制数位精度，或者
#  - 用户希望计算结果与手算相符的场合。
from decimal import *