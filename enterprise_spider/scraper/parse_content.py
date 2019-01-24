import re

from bs4 import UnicodeDammit
from scrapy import Selector

#  解析网页正文部分的算法实现

RULE_TEXT = './text() | .//p[not(@style) or @style!="display: none;"]//text()[not(ancestor::li) and not(' \
            'parent::script) and not(parent::a) and not(parent::style)] | .//div/text()[not(ancestor::li)] '


class ParseContent(object):
    EXCLU_DIVS = ['footer', 'bottom']  # 被排除的div class name
    THRESHOLD = 0.5

    @classmethod
    def search_content_xpath(cls, sel, exclu_divs):
        root = sel.xpath('/html/body')
        xpath = cls.recursion('/html/body', root, cls.THRESHOLD, exclu_divs + cls.EXCLU_DIVS)
        print('----------------content path is %s' % xpath)
        return xpath

    @classmethod
    def guess_content(cls, div_sel):
        #  验证是不是内容div。。。还没想到好办法
        ct = div_sel.extract()
        if not ct:
            return False
        # add other condition here
        return True

    @classmethod
    def recursion(cls, path, root_node, threshold, EXCLU_DIVS):
        divs = root_node.xpath('./div')
        parent_len = cls.get_text_len(root_node)
        max_div_index = 0
        max_len = 0
        if divs.__len__() == 0:
            return path
        for i in range(divs.__len__()):
            div = divs[i]
            class_name = div.xpath('./@class').extract_first()
            if class_name in EXCLU_DIVS:
                continue
            _len = cls.get_text_len(div)
            if _len > max_len:
                max_len = _len
                max_div_index = i
        max_div = divs[max_div_index]
        if max_len / (parent_len+1) < threshold:
            return path
        else:
            div_class = max_div.xpath('./@class').extract_first()
            div_id = max_div.xpath('./@id').extract_first()
            pos = str(max_div_index+1)
            if div_class:
                pos = '@class="' + div_class + '"'
            elif div_id:
                pos = '@id="' + div_id + '"'
            return cls.recursion(path + '/div[' + pos + ']', max_div, threshold, EXCLU_DIVS)

    @classmethod
    def get_text_len(cls, label):
        texts = label.xpath(RULE_TEXT).extract()
        text_join = ''.join(texts)
        text_join = re.sub('[^\u4e00-\u9fa5]', '', text_join)
        return len(text_join)
