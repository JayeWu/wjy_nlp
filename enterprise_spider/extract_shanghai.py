import os
import re

filename = 'D:\\rde\\data\\gs_html\\shanghai_list\\list.txt'
filename2 = './shanghai_list.txt'
with open(filename, 'r', encoding='utf8') as f:
    line = f.readline()
    set1 = set([])
    while line:
        gs = re.findall('(?<=val2:").*(?=",)', line)
        if gs:
            print(gs[0])
            set1.add(gs[0])
        line = f.readline()

with open(filename2, 'w', encoding='utf8') as f:
    for gs in set1:
        f.write(gs)
        f.write('\n')
