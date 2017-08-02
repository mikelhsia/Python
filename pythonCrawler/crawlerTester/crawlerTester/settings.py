# -*- coding: utf-8 -*-

# Scrapy settings for crawlerTester project
#
# This is so called "Project settings module" in Scrapy's official documentation
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

##########################################################################
# The name of the bot implemented by this Scrapy project (also known as the project name).
# This will be used to construct the User-Agent by default, and also for logging.
# It’s automatically populated with your project name when you create your project with the startproject command.
##########################################################################
BOT_NAME = 'crawlerTester'

##########################################################################
# A list of modules where Scrapy will look for spiders.
##########################################################################
SPIDER_MODULES = ['crawlerTester.spiders']

##########################################################################
# Module where to create new spiders using the genspider command.
##########################################################################
NEWSPIDER_MODULE = 'crawlerTester.spiders'

##########################################################################
# Crawl responsibly by identifying yourself (and your website) on the user-agent
##########################################################################
# USER_AGENT = 'crawlerTester (+http://www.yourdomain.com)'
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
# }

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

##########################################################################
# Maximum number of concurrent items (per response) to process in
# parallel in the Item Processor (also known as the Item Pipeline).
##########################################################################
# CONCURRENT_ITEMS = 100
# DEFAULT_ITEM_CLASS = 'scrapy.item.Item'

##########################################################################
# Configure maximum concurrent requests performed by Scrapy (default: 16)
##########################################################################
# CONCURRENT_REQUESTS = 32
# CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 8

##########################################################################
# Configure a delay for requests for the same website (default: 0)
# This setting is also affected by the RANDOMIZE_DOWNLOAD_DELAY setting (which is enabled by default).
# By default, Scrapy doesn’t wait a fixed amount of time between requests, but uses a random interval
# between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY.
# When CONCURRENT_REQUESTS_PER_IP is non-zero, delays are enforced per ip address instead of per domain.
##########################################################################
DOWNLOAD_DELAY = 0.25
# RANDOMIZE_DOWNLOAD_DELAY = True

##########################################################################
# The download delay setting will honor only one of:
##########################################################################
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Configure the limit of yield depth
DEPTH_LIMIT = 2
##########################################################################
# An integer that is used to adjust the request priority based on its depth:
#   if zero (default), no priority adjustment is made from depth
#   a positive value will decrease the priority, i.e. higher depth requests will be processed later ;
#   this is commonly used when doing breadth-first crawls (BFO)
#   a negative value will increase priority, i.e., higher depth requests will be processed sooner (DFO)
##########################################################################
# DEPTH_PRIORITY = 0

##########################################################################
# The class used to detect and filter duplicate requests.
# The default (RFPDupeFilter) filters based on request fingerprint using the
# scrapy.utils.request.request_fingerprint function.
##########################################################################
# DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

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
#    'crawlerTester.middlewares.CrawlertesterSpiderMiddleware': 543,
#}

##########################################################################
# The downloader to use for crawling.
##########################################################################
# DOWNLOADER = 'scrapy.core.downloader.Downloader'

##########################################################################
# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
##########################################################################
# DOWNLOADER_MIDDLEWARES = {
#    'crawlerTester.middlewares.MyCustomDownloaderMiddleware': 543,
# }
# DOWNLOAD_HANDLERS_BASE = {
#     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
#     'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
#     'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
#     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
#     'ftp': 'scrapy.core.downloader.handlers.ftp.FTPDownloadHandler',
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

##########################################################################
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
##########################################################################
# ITEM_PIPELINES = {
#    'crawlerTester.pipelines.CrawlertesterPipeline': 300,
# }

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

##########################################################################
# DNS related settings
##########################################################################
# DNSCACHE_ENABLED = True
# DNSCACHE_SIZE = 10000
# DNS_TIMEOUT = 60


##########################################################################
# Log setting
# File name to use for logging output. If None, standard error will be used.
##########################################################################
# LOG_ENABLED = True
# LOG_FILE = None
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'


##########################################################################
# Whether to enable memory debugging.
##########################################################################
MEMDEBUG_ENABLED = False