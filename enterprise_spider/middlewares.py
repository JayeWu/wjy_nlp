# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import re
import time

import requests
from scrapy import signals
from scrapy.http import HtmlResponse

from enterprise_spider.user_agent import agents


class EnterpriseSpiderSpiderMiddleware(object):
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


class EnterpriseSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, ips):
        self.ips = ips

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(ips={'106.57.7.178:4528': 3, '60.188.38.98:4541': 3, '113.121.146.210:4523': 3,
                        '39.66.12.155:4574': 3, '27.40.132.26:4538': 3, '122.246.164.134:4575': 3,
                        '182.34.32.216:4566': 3, '59.62.25.143:4518': 3})

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if len(self.ips) < 8:
            while True:
                time.sleep(1.2)
                ip = requests.get(
                    "http://d.jghttp.golangapi.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=").text.strip()
                if re.match('[\d\.]+:\d+', ip):
                    self.ips[ip] = 3
                    break
        ip_list = [ip for ip in self.ips.keys()]
        ip = random.choice(ip_list)

        print(self.ips)
        request.meta['proxy'] = ip
        return None

    def process_response(self, request, response, spider):
        if response.status == '403':
            ip = request.meta['proxy'][2:]
            if ip in self.ips:
                self.ips[ip] -= 1
            if self.ips[ip] == 0:
                self.ips.remove(ip)
            request.meta['proxy'] = random.choice(self.ips)
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        print(exception)
        # print(request.meta['proxy'])
        if request.meta['proxy'][2:] in self.ips:
            self.ips.remove(request.meta['proxy'][2:])
        print(self.ips)
        print('------------')
        return None

        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        while True:
            time.sleep(2)
            ip = requests.get(
                "http://d.jghttp.golangapi.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=4100&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=").text
            if re.match('[\d\.]+:\d+', ip):
                break
        print(ip)
        request.meta['proxy'] = ip
