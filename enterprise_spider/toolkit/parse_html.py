import json
import logging
import random
import re
import time
from urllib.parse import urlencode, quote

from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
import os

#  解析网页文本， 分句子
THRESHOLD = 15


def txt_from_html(html):
    sel = Selector(text=html)
    txts = sel.xpath('.//text()').extract()
    txts = [x.strip() for x in txts]
    text = [x for x in txts if x and len(x) > THRESHOLD]
    return ' '.join(text)


def split_sentence(content):
    sens = re.split('[。！？!?\n\r]', content)
    sens = [re.sub('[^\u4e00-\u9fa5]{20,}', '', x) for x in sens]
    sens = [x for x in sens if len(x) > THRESHOLD]
    return sens
