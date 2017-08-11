# -*- coding: utf-8 -*-

# Scrapy settings for scrapyItemLoader project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapyItemLoader'

SPIDER_MODULES = ['scrapyItemLoader.spiders']
NEWSPIDER_MODULE = 'scrapyItemLoader.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyItemLoader (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Configure the limit of yield depth
DEPTH_LIMIT = 20

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapyItemLoader.middlewares.ScrapyitemloaderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapyItemLoader.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	# 后面的数字代表执行优先级 ，当执行pipeine的时候会按照数字由小到大执行
	# 通常将这些数字定义在0-1000范围内。
	'scrapyItemLoader.pipelines.ScrapyitemloaderPipeline': 300,
	# 'scrapy.pipelines.images.ImagesPipeline': 400,
	# 'scrapy.pipelines.files.FilesPipeline': 500,
}
# Then, configure the target storage setting to a valid value that will be used for storing the downloaded images.
# Otherwise the pipeline will remain disabled, even if you include it in the ITEM_PIPELINES setting.
# The files are stored using a SHA1 hash of their URLs for the file names.
# For the Files Pipeline, set the FILES_STORE setting:
# FILES_STORE = '/Users/tsuyuhsia/Desktop/Python'
# # For the Images Pipeline, set the IMAGES_STORE setting:
# IMAGES_STORE = '/Users/tsuyuhsia/Desktop/Python'

# # For the Files Pipeline, set FILES_URLS_FIELD and/or FILES_RESULT_FIELD settings:
# FILES_URLS_FIELD = 'imgSrc'
# FILES_RESULT_FIELD = 'imgDst'
# # For the Images Pipeline, set IMAGES_URLS_FIELD and/or IMAGES_RESULT_FIELD settings:
# IMAGES_URLS_FIELD = 'imgSrc'
# IMAGES_RESULT_FIELD = 'imgDst'

# # 120 days of delay for files expiration. Default is 90
# FILES_EXPIRES = 120
# # 30 days of delay for images expiration. Default is 90
# IMAGES_EXPIRES = 30

# # Generating thumbnail
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }

# # Filtering out small images
# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110


##############################################################################
# IMAGES_URLS_FIELD ="image_url"  #image_url是在items.py中配置的网络爬取得图片地址 
# - 配置保存本地的地址
# project_dir=os.path.abspath(os.path.dirname(__file__))  #获取当前爬虫项目的绝对路径
# IMAGES_STORE=os.path.join(project_dir,'images')  #组装新的图片路径
# 　还有很多设置有特殊需要的话可以用哦 （详情可以去imagepipeine源码查看）
#    IMAGES_MIN_HEIGHT=100   #设定下载图片的最小高度
#    IMAGES_MIN_WIDTH=100　　#设定下载图片的最小宽度
##############################################################################

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
