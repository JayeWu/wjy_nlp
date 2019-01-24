from pyhanlp import *
import os
import shutil
import traceback

import gevent
from scrapy import Request, Selector
import json
import logging
import random
import re


def get_person_names(text):
    PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
    analyzer = PerceptronLexicalAnalyzer()
    words = analyzer.analyze(text)
    # print(words)
    words = str(words)
    names = re.findall(' \w*(?=/nr)', words)
    name_set = set([])
    for name in names:
        name_set.add(name)
    print(name_set)
    return name_set


texts = open('D:\\rde\data\search_by_baidu\co2ceo_sentences3/电通+李静宜.txt', 'r', encoding='utf8').read()
get_person_names(texts)
