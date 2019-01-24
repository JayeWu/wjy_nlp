import os
import re

#  去除文本中大段的 代码
dir_ = 'D:\\rde\\data\\search_by_baidu\\co2ceo_sentences2'
dir_2 = 'D:\\rde\\data\\search_by_baidu\\co2ceo_sentences3'

fileList = os.listdir(dir_)

for file in fileList:
    file2 = os.path.join(dir_2, file)
    file = os.path.join(dir_, file)
    text = open(file, 'r', encoding='utf8').read()
    # text = re.sub('[^\u4e00-\u9fa5]{20,}', '', text)
    text = re.sub(' {4,}', '', text)
    open(file2, 'w', encoding='utf8').write(text)
