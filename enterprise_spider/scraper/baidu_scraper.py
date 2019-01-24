import os
import shutil
import traceback

import gevent
from scrapy import Request, Selector
import json
import logging
import random
import re

#  刮取百度百科的结构化信息


from enterprise_spider.toolkit.savefile import savefile

SEPARATOR = '\n&&&&&'


def baidu_scraper():
    dir_baidu = 'D:\\rde\\data\\baidu_html_abbre'
    dir_list = os.listdir(dir_baidu)
    file = ''
    for dir_ in dir_list:
        gs_dir = os.path.join(dir_baidu, dir_)
        file_list = os.listdir(gs_dir)
        if file_list:
            for i in file_list:
                if os.path.isfile(os.path.join(gs_dir, i)):
                    file = i
                    break
        if not file:
            continue
        name = dir_
        file = os.path.join(gs_dir, file)
        # if re.search('全球最大', file):
        #     shutil.rmtree(os.path.join(dir_baidu, dir_))
        # continue
        text = open(file, 'r', encoding='utf8').read()
        # print(text)
        labels = '(a|img|i)'
        reg = '(\n*<'+labels+'[^>]*>)|(</'+labels+'>\n*)|(&nbsp;)'
        text = re.sub(reg, '', text)
        sel = Selector(text=text)
        div_texts = [''.join([x.strip() for x in div.xpath('./text()').extract() if x.strip()]) for div in sel.xpath('//div[@class="main-content"]//div[@class="para"]')]
        # print(div_texts)
        texts = SEPARATOR.join(x for x in div_texts if re.match('^.*[\.。？！?!]$', x.strip()))
        # texts = SEPARATOR.join([x.strip() for x in sel.xpath('//div[@class="main-content"]//text()').extract() if
        #                         re.match('^.*[\.。？！?!]$', x.strip()) and len(x.strip().encode('utf8')) > 10])
        # texts = SEPARATOR.join([x.strip() for x in div_texts if re.match('^.*[\.。？！?!]$', x.strip()) and len(x.strip().encode('utf8')) > 10])
        savefile('D:/rde/data/pure_text_abbre/' + name.split('.html')[0] + '.txt', texts)
        # savefile('D:/rde/data/pure_text_all/' + name, text)
        # print(texts)
        # extract_data(sel, name)


def extract_data(sel, name):
    basic_info_sel = sel.xpath('//div[contains(@class, "basic-info")]')
    if not basic_info_sel:
        return
    dts = basic_info_sel.xpath('.//dt')

    dts_text = [''.join([re.sub('\s', '', i).strip() for i in dt.xpath('.//text()').extract()]) for dt in dts]

    dds = basic_info_sel.xpath('.//dd')
    dds_text = [''.join([re.sub('\s', '', i).strip() for i in dd.xpath('.//text()').extract()]) for dd in dds]

    basic_info_list = zip(dts_text, dds_text)
    basic_info = '\n'.join([dt.strip() + ':' + dd.strip() for dt, dd in basic_info_list])
    file_extract = os.path.join('D:\\rde\\data\\baidu_text', name.split('.html')[0] + '.txt')
    f = open(file_extract, 'w', encoding='utf8')
    f.write(basic_info)
    print(name)
    f.close()


baidu_scraper()
