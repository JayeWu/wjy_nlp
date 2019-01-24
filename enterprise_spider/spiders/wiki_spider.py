import time
from urllib.parse import urlencode, quote

from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
import os


def get_gs_set():
    set1 = set([])
    with open('D:\\rde\\enterprise_spider\\enterprise_spider\\data\\all_list.txt', 'r', encoding='utf8') as f:
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


def isSimilar(a, b):
    score = 0
    for char in a:
        if char in b:
            score += 1
    return score >= len(a) * 0.6


#  wiki爬虫
class WikiSpider(CrawlSpider):
    name = "wiki_spider"
    start_urls = "https://zh.wikipedia.org/"
    items = get_gs_set()
    # print(items)
    html_dir = "D://rde/data/wiki_html_all"
    os.makedirs(html_dir, exist_ok=True)

    def start_requests(self):
        for item in self.items:
            item = item.strip()
            time.sleep(1)
            item_encode = quote(item)
            url = 'https://zh.wikipedia.org/w/index.php?title=Special:%E6%90%9C%E7%B4%A2&search=' + item_encode
            # url = self.start_urls + 'item/' + item_encode
            print(url)
            yield Request(url=url, meta={'item': item}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = response.meta['item']
        title_as = response.xpath(
            "/html/body//ul[@class='mw-search-results']/li[@class='mw-search-result']/div[@class='mw-search-result-heading']/a")
        url = ''
        for i in range(len(title_as)):
            if i > 5:
                return
            title = title_as[i].xpath('./text()').extract_first()
            if isSimilar(title, item):
                url = title_as[i].xpath('./@href').extract_first()
                break
        if not url:
            return
        url = response.urljoin(url)
        yield Request(url=url, meta={'item': item}, callback=self.parse1)

    def parse1(self, response):
        text = response.text
        item = response.meta['item']
        print("%s is scrawled " % item)
        filename = self.html_dir + '/' + item + '.html'
        savefile(filename, text)
