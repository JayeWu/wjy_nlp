import os

filelist = ['ny_list.txt','quc_shenzhen.txt','quc.txt']

set1 = set([])
for ff in filelist:
    with open(ff, 'r', encoding='utf8') as f:
        gs = f.readline()
        while gs:
            set1.add(gs)
            gs = f.readline()

with open('./all_list.txt', 'w', encoding='utf8') as f:
    for gs in set1:
        f.write(gs.strip())
        f.write('\n')
