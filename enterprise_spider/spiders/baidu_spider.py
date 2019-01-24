import json
import logging
import random
import re
import time
from urllib.parse import urlencode, quote

from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
import os

cookies = {
    "BIDUPSID": "118151B90329FA805B430E34388DB12E",
    "PSTM": "1542071441",
    "BAIDUID": "10422135DA87A82D92AA80B9BED992BE:FG=1",
    "BDUSS": "ZDME1IQTZqdHE5eXJaNUp2OTJ5WEdrdHFGdFRNTS1nQjUyTUlrWTQwVmtsa0ZjQVFBQUFBJCQAAAAAAAAAAAEAAAB2G-QozuLS7czswfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGQJGlxkCRpcdT",
    "BDORZ": "FFFB88E999055A3F8A630C64834BD6D0",
    "MCITY": "-315%3A",
    "BDSFRCVID": "8PkOJeC62GdKxi398ex7bQjiS2A72enTH6aopSjccmqwpLgrVLhVEG0Pjx8g0KAb-qhEogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0P3J",
    "H_BDCLCKID_SF": "tJP8oDDbtCL3fP36q46EbnL_hxJb54cQ24o2WbCQfUJO8pcNLTDKQP0U2Mueq6v-MnvabRcVLKoNMIoNhlO1j4_eKbbB5-JL-6vj2n3-QqRsSl5jDh3825ksD-RC5DrD2gTy0hvcBIocShnzBUjrDRLbXU6BK5vPbNcZ0l8K3l02VKO_e4bK-Tr3eHKJJx5",
    "Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a": "1547687071,1547717093,1547778072,1547778228",
    "delPer": "0",
    "PSINO": "3",
    "BDRCVFR[g0wo5JS-3Js]": "mk3SLVN4HKm",
    "H_PS_PSSID": "",
    "BKWPF": "3",
    "pgv_pvi": "6642073600",
    "pgv_si": "s8202748928",
    "Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a": "1547794599"
}
#  爬取百度百科

def get_gs_set():
    set1 = set([])
    with open('./data/it_name_list.txt', 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            set1.add(line)
            line = f.readline()
    return set1


def savefile(filename, text):
    dir = '/'.join(filename.split('/')[:-1])
    os.makedirs(dir, exist_ok=True)
    with open(filename, 'w', encoding='utf8') as f:
        f.write(text)


class BaiduSpider(CrawlSpider):
    name = "baidu_spider"
    start_urls = "https://baike.baidu.com/"
    items = get_gs_set()
    html_dir = "D://rde/data/baidu_html_abbre"
    os.makedirs(html_dir, exist_ok=True)

    def start_requests(self):
        for item in self.items:
            item = item.strip()
            time.sleep(1)
            item_encode = quote(item)
            url = self.start_urls + 'item/' + item_encode
            yield Request(url=url, meta={'url': url, 'item': item}, callback=self.parse,
                          dont_filter=True)

    def parse(self, response):
        text = response.text
        requesturl = response.meta['url']
        item = response.meta['item']
        if requesturl != response.url:
            print('---------------redirected ,retrying--------------')
            url = response.url
            yield Request(url=url, meta={'url': url, 'item': item}, callback=self.parse,)

        title = response.xpath('/html/head/title/text()').extract_first()
        if (not title) or re.search("全球最大中文百科全书", title.strip()) or not isinstance(title, str):
            print('item %s not founded' % item)
            return
        title = re.sub('[\s\\\/:*?"<>|]+', '', title)
        print('baidu pedia item %s scrawled' % title)
        savefile(self.html_dir + '/' + item + '/' + title + '.html', text)

        reference_urls = response.xpath('/html/body//ul[@class="reference-list"]/li/a[@rel="nofollow"]/@href').extract()
        for url in reference_urls:
            url = response.urljoin(url)
            yield Request(url=url, meta={"url": url, "item": item}, callback=self.parse_ref)

    def parse_ref(self, response):
        text = response.text
        item = response.meta['item']
        requesturl = response.meta['url']
        if requesturl != response.url:
            print('--------------- redirected ,retrying--------------')
            url = response.url
            yield Request(url=url, meta={'url': url, 'item': item}, callback=self.parse_ref)
        else:
            title = response.xpath('/html/head/title/text()').extract_first()
            if not title:
                print('---------------baidu redirected ,retrying--------------')
                redirect_url = re.findall("(?<=URL=\')[a-zA-z]+://[^\s\']*(?=\'\">)", response.text)
                if redirect_url:
                    url = redirect_url[0]
                    yield Request(url=url, meta={'url': url, 'item': item}, callback=self.parse_ref)
            else:
                print('baidu pedia item %s reference %s scrawled' % (item, title))
                if isinstance(title, str):
                    title = re.sub('[\s\\\/:*?"<>|]+', '', title)
                    savefile(self.html_dir + '/' + item + '/refs/' + title + '.html', text)
