import json
import logging
import random
import re
import time

from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
import os

gs_list_filename = './gs_list_kanzhun.txt'
# gs_list_filename = './gs_list_shenzhen.txt'

#  爬取看准网，深圳交易所等网站的 公司列表，并存网页
cookieses = [
    {
        "W_CITY_S_V": "2",
        "_f_k":"reborn",
        "aliyungf_tc": "AQAAAGOX7yqHggQAD1XheVF1ECchZjqK", "AB_T": "abvb",
        "__c": "1547772516",
        "__g": "-",
        "__l=1": "%2Fwww.kanzhun.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DmmB-leopLDhW0rJPnYn24qlu71zXkwwgReYQRJWFw-7UIQ5wE7c4UEm2q9qCWYrF%26wd%3D%26eqid%3De6d1588300031400000000055c412263",
        "Hm_lvt_1f6f005d03f3c4d854faec87a0bee48e": "1546050815,1547687412",
        "isHasPushRecommentMessage": "true",
        "thirtyMinutes": "true",
        "thirtyMinutesCount": "4",
        "__a": "22906260.1546050815.1546050815.1547687412.23.2.15.23",
        "Hm_lpvt_1f6f005d03f3c4d854faec87a0bee48e": "1547691103"
    }, {
        "W_CITY_S_V=2; _f_k=reborn; aliyungf_tc=AQAAAGOX7yqHggQAD1XheVF1ECchZjqK; AB_T=abvb; __c=1547772516; __g=-; __l=l=; Hm_lvt_1f6f005d03f3c4d854faec87a0bee48e=1547696098,1547772516,1547772963,1547772982; isHasPushRecommentMessage=true; thirtyMinutes=true; thirtyMinutesCount=1; __a=22906260.1546050815.1547687412.1547772516.102.3.10.24; Hm_lpvt_1f6f005d03f3c4d854faec87a0bee48e=1547773128"
    }
]


def appendListFile(gs_list):
    with open(gs_list_filename, 'a', encoding='utf8') as f:
        for i in gs_list:
            f.write('\r\n')
            f.write(i)


def savefile(filename, text):
    dir = '/'.join(filename.split('/')[:-1])
    os.makedirs(dir, exist_ok=True)
    with open(filename, 'w', encoding='utf8') as f:
        f.write(text)


class ListSpider(CrawlSpider):
    name = "list_spider"
    allowed_domains = ["kanzhun.com", "sse.com.cn", "szse.cn", "sc.hkex.com.hk"]
    kanzhun_urls = [
                    # "/plc52p1.html",
                    # "/plc65p1.html",
                    # "/plc67p1.html",
                    # "/plc64p1.html",
                    # "/plc62p1.html",
                    # "/plc54p1.html",
                    # "/plc53p1.html",
                    # "/plc57p1.html",
                    # "/plc58p1.html",
                    # "/plc61p1.html",
                    # "/plc66p1.html",
                    "/companyl/search/?q=&pagenum=10",
                    # "/plc63p1.html",
                    # "/plc56p1.html",
                    # "/plc60p1.html",
                    # "/plc59p1.html",
                    # "/plc55p1.html",
                    # "/plc129p1.html"
    ]
    start_urls = [
        "https://www.kanzhun.com",
        # "https://www.kanzhun.com/companyl/search/?q=&pagenum=1"
        # "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110x&TABKEY=tab1&PAGENO=45",
        # "http://www.sse.com.cn/assortment/stock/list/share/",
        # "https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=zh-cn&sort=0"
    ]
    html_dir = "D://rde/data/kanzhun_html_remen"
    os.makedirs(html_dir, exist_ok=True)

    def start_requests(self):
        parses = [self.parse1, self.parse2, self.parse3, self.parse4]
        for i in range(len(self.kanzhun_urls)):
            url = self.kanzhun_urls[i]
            yield Request(url="https://www.kanzhun.com" + url, cookies=cookieses[0], callback=parses[0],
                          dont_filter=True)

        # yield Request(url=self.start_urls[1], cookies=cookieses[1], callback=parses[1], dont_filter=True)

    def parse_info(self, response):
        title = response.xpath("/html/head/title/text()").extract_first()
        if isinstance(title, str):
            title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', title)
        else:
            title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', response.url)
        filename = self.html_dir + '/kanzhun_all/' + title + '.html'
        savefile(filename, response.text)

    def parse_info2(self, response):
        title = response.meta["name"]
        if isinstance(title, str):
            title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', title)
        else:
            title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', response.url)
        filename = self.html_dir + '/shenzhen_info/' + title + '.txt'
        savefile(filename, response.text)

    def parse1(self, response):
        filename = self.html_dir+'/'+response.url[-1]
        savefile(filename, response.text)
        gs_list = response.xpath("/html/body//ul[@class='company_result "
                                 "']/li/div/a[1]/text()").extract()
        appendListFile(gs_list)
        print(gs_list)
        info_urls = response.xpath(
            "/html/body[@class='grey-bg']//ul[@class='company_result ']/li/div/a[1]/@href").extract()
        print(info_urls)
        for url in info_urls:
            url = response.urljoin(url)
            yield Request(url=url, cookies=cookieses[0], callback=self.parse_info)
        next_url = response.xpath("/html/body//a[@class='p_next']/@href").extract_first()
        print(next_url)
        if next_url:
            yield Request(url=response.urljoin(next_url), callback=self.parse1)

    def parse2(self, response):
        json_text = json.loads(response.text)
        data = json_text[0]['data']
        gs_list = [item['gsqc'] for item in data]
        info_code_list = [re.findall('(?<=code=)\d+', item['gsjc'])[0] for item in data]
        for code, name in zip(info_code_list, gs_list):
            url = 'http://www.szse.cn/api/report/index/companyGeneralization?random=0.9912233244487931&secCode='+str(code)
            yield Request(url=url, meta={"name": name}, callback=self.parse_info2)
        appendListFile(gs_list)
        print(gs_list)
        next_page = int(re.findall('(?<=PAGENO=)\d+', response.url)[0]) + 1
        filename = '深圳证券所_'+str(next_page)+'.txt'
        filename = self.html_dir + '/shenzhen_list/'+filename
        savefile(filename, response.text)
        next_url = re.sub('(?<=PAGENO=)\d+', str(next_page), response.url)
        yield Request(url=next_url, callback=self.parse2, dont_filter=True)

    def parse3(self, response):
        pass

    def parse4(self, response):
        pass
