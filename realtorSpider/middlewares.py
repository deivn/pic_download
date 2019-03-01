# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64
import time
from scrapy.conf import settings
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse

# js = """
# function scrollToBottom() {
#
#     var Height = document.body.clientHeight,  //文本高度
#         screenHeight = window.innerHeight,  //屏幕高度
#         INTERVAL = 100,  // 滚动动作之间的间隔时间
#         delta = 500,  //每次滚动距离
#         curScrollTop = 0;    //当前window.scrollTop 值
#
#     var scroll = function () {
#         curScrollTop = document.body.scrollTop;
#         window.scrollTo(0,curScrollTop + delta);
#     };
#
#     var timer = setInterval(function () {
#         var curHeight = curScrollTop + screenHeight;
#         if (curHeight >= Height){   //滚动到页面底部时，结束滚动
#             clearInterval(timer);
#         }
#         scroll();
#     }, INTERVAL)
# }
# scrollToBottom()
# """

# USER-AGENT中间件代理类


class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # 加载IPLIST
        return cls(settings['USER_AGENTS'])

    # 该方法在引擎发送http request请求给下载器时会经过下载中间件，可以设置ip代理，User-Agent, 设置关闭cookie
    def process_request(self, request, spider):
        """
        从配置文件读取user-agent池中的数据，每次请求都随机选一个user-agent
        :param request: 在引擎发送给下载器的http request请求
        :param spider: 引擎
        :return:
        """
        useragent = random.choice(self.agents)
        request.headers.setdefault("User-Agent", useragent)


class PhantomJSMiddleware(object):

    def __init__(self, driver):
        self.driver = driver

    @classmethod
    def from_crawler(cls, crawler):
        driver = webdriver.PhantomJS(executable_path='D:\\devtools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')  # 指定使用的浏览器
        return cls(driver)


    def process_request(self, request, spider):
        # flag = request.meta.get('PhantomJS')
        if spider.name == 'realtor':
            "PhantomJS is starting..."
            self.driver.get(request.url)
            time.sleep(1)
            js = "var q=document.documentElement.scrollTop=10000"
            self.driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(3)
            body = self.driver.page_source
            # driver.save_screenshot('1.png')
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return

    def process_response(self, request, response, spider):
        return response


'''
动态设置代理ip
'''


class RandomProxy:

    def __init__(self, iplist):
        self.iplist = iplist

    @classmethod
    def from_crawler(cls, crawler):
        # 加载IPLIST
        return cls(settings['IPLIST'])

    def process_request(self, request, spider):
        proxy = random.choice(self.iplist)


class RandomProxy(object):

    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        # 加载IPLIST
        return cls(settings['PROXIES'])

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)

        if proxy['user_pass'] is None:
            # 没有代理账户验证的代理使用方式
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
        else:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.b64encode(proxy['user_pass'].encode('utf-8'))
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass.decode()



class ForsalecrawlSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ForsalecrawlDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
