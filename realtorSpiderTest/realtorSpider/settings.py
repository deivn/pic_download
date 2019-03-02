# -*- coding: utf-8 -*-

# Scrapy settings for realtorSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'realtorSpider'

SPIDER_MODULES = ['realtorSpider.spiders']
NEWSPIDER_MODULE = 'realtorSpider.spiders'

# 数据保存路径
DATA_PATH_PREFIX = "D:/house/data/realtor"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'realtorSpider (+http://www.yourdomain.com)'

# 默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
DUPEFILTER_DEBUG = True
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 关掉重定向, 不会重定向到新的地址
REDIRECT_ENABLED = False
# 返回301, 302时, 按正常返回对待, 可以正常写入cookie
# HTTPERROR_ALLOWED_CODES = [301, 302]

# PHANTOMJS_PATH = 'D:\\devtools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'

# mysql配置参数
# MYSQL_HOST = "ebuyhouse.ckzejnyrspwg.us-west-2.rds.amazonaws.com"
# MYSQL_PORT = 3306
# MYSQL_USER = "ebuyhouse"
# MYSQL_PASSWD = "ebuyhouse421"
# MYSQL_DB = "ebuyhouse_produce"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWD = "root"
MYSQL_DB = "python_data"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Connection': 'keep-alive',
#     'cookie': 'JSESSIONID=b3c4a6e8ca5a1e67',
#     'Host': 'www.realtor.com',
#     'Origin': 'https://www.realtor.com',
#     'Referer': 'https://www.realtor.com/?tdsourcetag=s_pctim_aiomsg',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'realtorSpider.middlewares.RealtorspiderSpiderMiddleware': 543,
#}

# 下载中间件配置User-Agent池
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 代理
# PROXIES = [
#     {'ip_port': '61.178.238.122:63000', 'user_pass': ''}, {'ip_port': '117.114.149.66:53281', 'user_pass': ''},
#     {'ip_port': '61.138.33.20:808', 'user_pass': ''}, {'ip_port': '61.135.217.7:80', 'user_pass': ''},
#     {'ip_port': '27.17.45.90:43411', 'user_pass': ''}, {'ip_port': '118.122.92.252:37901', 'user_pass': ''},
#     {'ip_port': '219.238.186.188:8118', 'user_pass': ''}, {'ip_port': '61.164.39.69:53281', 'user_pass': ''},
#     {'ip_port': '60.191.201.38:45461', 'user_pass': ''}, {'ip_port': '113.108.242.36:47713', 'user_pass': ''},
#     {'ip_port': '117.191.11.107:80', 'user_pass': ''}, {'ip_port': '106.14.176.162:80', 'user_pass': ''},
#     {'ip_port': '163.125.251.144:8118', 'user_pass': ''}, {'ip_port': '119.179.137.217:8060', 'user_pass': ''},
#     {'ip_port': '111.230.254.195:8118', 'user_pass': ''}
# ]
# 代理服务器
# proxyServer = "http://http-dyn.abuyun.com:9020"
PROXY_SERVER = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
# proxyUser = "H012345678901zyx"
# proxyPass = "0123456789012xyz"
PROXY_USER= "H012345678901zyx"
PROXY_PASS= "0123456789012xyz"

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'realtorSpider.middlewares.RandomUserAgent': 542,
    'realtorSpider.middlewares.RandomProxy': 543,
    'realtorSpider.middlewares.PhantomJSMiddleware': 544,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'realtorSpider.pipelines.RealtorspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
