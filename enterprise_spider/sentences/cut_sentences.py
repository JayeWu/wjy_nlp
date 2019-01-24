import os
import shutil
import traceback

import gevent
from scrapy import Request, Selector
import json
import logging
import random
import re

from enterprise_spider.toolkit.savefile import savefile

ER_symbol = '$ER2$'  # 代替实体的符号
SPAN = 50  # 截取宽度
PATCH = '#'

in_dir = 'D:\\rde\\data\\search_by_baidu\\co2ceo_sentences3'
out_dir = 'D:\\rde\\data\\search_by_baidu\\ceo_samelen_sentences'

filelist = os.listdir(in_dir)
print(filelist)

for file in filelist:
    sent_list = []
    er = file.split('.txt')[0].split('+')[-1]
    file_out = os.path.join(out_dir, file)
    file_in = os.path.join(in_dir, file)

    with open(file_in, 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            line = line.strip()
            # line = line.replace(er, ER_symbol)
            sear = re.search(er, line)
            if sear:
                span = sear.span()
                left = span[0] - SPAN
                left = left if left > 0 else 0
                if len(line)-left >= SPAN*2 + len(ER_symbol):
                    line = line.replace(er, ER_symbol, 1)
                    cut = line[left:left + SPAN*2 + len(ER_symbol)]
                else:
                    right = span[1] + SPAN
                    right = right if right < len(line) else len(line)
                    cut = line[left:right]
                    cut = cut.replace(er, ER_symbol, 1)
                    cut = PATCH * (left - span[0] + SPAN) + cut + PATCH * (span[1] + SPAN - right)
                print(len(cut), cut)
                sent_list.append(cut)
            line = f.readline()

    savefile(file_out, '\n'.join(sent_list), 'w')
