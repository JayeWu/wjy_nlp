import json
import logging
import random
import re
import time
from urllib.parse import urlencode, quote

from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
import os

from sqlalchemy.orm import sessionmaker

from enterprise_spider.scraper.kanzhun_scraper import engine, Company
from enterprise_spider.scraper.parse_content import ParseContent
from enterprise_spider.toolkit.parse_html import txt_from_html, split_sentence
from enterprise_spider.toolkit.savefile import savefile


#  搜索百度新闻，爬取相关数据
def get_gs_set():
    set1 = set([])
    with open('./data/less_list.txt', 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            if line.strip():
                set1.add(line)
            line = f.readline()
    return set1


def get_companyfield():
    list1 = []
    with open('./data/less_list.txt', 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            if line.strip():
                Session = sessionmaker(bind=engine)
                sess = Session()
                line = line.strip()
                comp = sess.query(Company).filter_by(co_abbre_name=line).first()
                sess.close()
                if not comp:
                    line = f.readline()
                    continue
                ceo = re.sub(r'[.()|?,，。<>、/\'\"《》！@#￥%…&*（）\\]', '', comp.co_ceo).strip()
                # city = re.sub(r'[.()|?,，。<>、/\'\"《》！@#￥%…&*（）\\]', '', comp.co_city).strip()

                if ceo.strip():
                    list1.append({'line': line, 'ceo': ceo})
            line = f.readline()
    # filelist = os.listdir('D:\\rde\\data\\search_by_baidu\\co2field_sentences2')
    # for file in filelist:
    #     ss = ''.join(file.split('.txt')[0].split(' '))
    #     set1.remove(ss)
    print(list1)
    return list1


class WebSpider(CrawlSpider):
    name = "web_spider"
    start_urls = "https://www.baidu.com/"
    # items = get_gs_set()
    co2field = get_companyfield()
    html_dir = "D://rde/data/search_by_baidu"
    os.makedirs(html_dir, exist_ok=True)

    def start_requests(self):

        # for item in self.items:
        #     item = item.strip()
        #     time.sleep(1)
        #     item_encode = quote(item)
        #     url = 'http://news.baidu.com/ns?word=' + item_encode + '&tn=news&from=news&cl=2&rn=50&ct=1'
        #     yield Request(url=url, meta={'url': url, 'item': item}, callback=self.parse,
        #                   dont_filter=True)
        for item in self.co2field:
            print(item)
            word = item['line'] + item['ceo']
            field = item['ceo']
            item_encode = quote(word)
            url = 'http://news.baidu.com/ns?word=' + item_encode + '&tn=news&from=news&cl=2&rn=30&ct=1'
            yield Request(url=url, meta={'url': url, 'item': item['line'], 'field': field}, callback=self.parse,
                          dont_filter=True)

    def parse(self, response):
        item = response.meta['item']
        field = response.meta['field']
        news_urls = response.xpath("/html/body//h3[@class='c-title']/a/@href").extract()
        for url in news_urls:
            yield Request(url=url, meta={'item': item, 'field': field}, callback=self.parse_news)

    def parse_news(self, response):
        text = response.text
        item = response.meta['item']
        field = response.meta['field']
        title = response.xpath('/html/head/title/text()').extract_first()
        title = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()\|?【】“”！，。？:：、~@#￥%……&*（）]+', '', title)
        savefile(self.html_dir + '/ceo_htmls/' + title + '.html', text)
        content_xpath = ParseContent().search_content_xpath(response, [])
        contents = response.xpath(content_xpath).extract_first()
        if not contents:
            return
        contents_txt = txt_from_html(contents)
        sentences = split_sentence(contents_txt)
        sentences = [x for x in sentences if re.search(field, x)]
        filename = self.html_dir + '/co2ceo_sentences2/' + item + '+' + field + '.txt'
        savefile(filename, '\n'.join(sentences), 'a')
