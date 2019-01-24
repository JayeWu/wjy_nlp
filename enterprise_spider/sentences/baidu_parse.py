import os
import shutil
import traceback

import gevent
from scrapy import Request, Selector
import json
import logging
import random
import re

from sqlalchemy.orm import sessionmaker

from enterprise_spider.scraper.kanzhun_scraper import Company, engine

#  解析百度百科正文 纯文本中的句子， 分类到 ceo， 法人代表， 总部城市关系 数据中
SEPARATOR = '\n&&&&&'

file_dir = "D:\\rde\\data\\pure_text_abbre"

fileList = os.listdir(file_dir)
ceo_file = 'D:\\rde\\extracted_data\\co2per\\ceo.txt'
com_rep_file = 'D:\\rde\\extracted_data\\co2per\\com_rep.txt'
city_file = 'D:\\rde\\extracted_data\\co2address\\city.txt'
f_ceo = open(ceo_file, 'a', encoding='utf8')
f_city = open(city_file, 'a', encoding='utf8')
f_rep = open(com_rep_file, 'a', encoding='utf8')

for file in fileList:
    name = file.split('.txt')[0]
    file = os.path.join(file_dir, file)
    texts = open(file, 'r', encoding='utf8').read()
    paras = texts.split(SEPARATOR)
    sentences = []
    for p in paras:
        sens = re.split('[。！？.!?]', p)
        sentences.extend(sens)
    sentences = [x.strip() for x in sentences if len(x) > 8]

    # open('D:\\rde\\extracted_data\\sentences\\'+name+'.txt', 'w', encoding='utf8').write('\n'.join(sentences))

    lens = [len(x) for x in sentences]
    Session = sessionmaker(bind=engine)
    sess = Session()
    comp = sess.query(Company).filter_by(co_abbre_name=name).first()
    if not comp:
        continue
    sess.close()
    co_city = re.sub(r'[.()|?,，。<>、/\'\"《》！@#￥%…&*（）\\]', '', comp.co_city)
    co_ceo = re.sub(r'[.()|?,，。<>、/\'\"《》！@#￥%…&*（）\\]', '', comp.co_CEO)
    com_rep = re.sub(r'[.()|?,，。<>、/\'\"《》！@#￥%…&*（）\\]', '', comp.com_rep)
    print(co_ceo, co_city, com_rep)
    ceos = []
    citys = []
    com_reps = []
    for sent in sentences:
        if co_city and re.search(co_city, sent):
            citys.append(sent + '\t&&&' + name + '\t&&&' + co_city+'\t&&&Positive')
        if co_ceo and re.search(co_ceo, sent):
            ceos.append(sent + '\t&&&' + name + '\t&&&' + co_ceo+'\t&&&Positive')
        if com_rep and re.search(com_rep, sent):
            com_reps.append(sent + '\t&&&' + name + '\t&&&' + com_rep+'\t&&&Positive')
    if ceos:
        f_ceo.write('\n'.join(ceos)+'\r\n')
    if citys:
        f_city.write('\n'.join(citys)+'\r\n')
    if com_reps:
        f_rep.write('\n'.join(com_reps)+'\r\n')

f_ceo.close()
f_city.close()
f_rep.close()
