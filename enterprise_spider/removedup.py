import os


filename = './gs_list_shenzhen.txt'
filename2 = './quc_shenzhen.txt'
with open(filename, 'r', encoding='utf8') as f:
    set1 = set([])
    gs = f.readline()
    while gs:
        set1.add(gs)
        gs = f.readline()

with open(filename, 'r', encoding='utf8') as f:
    set1 = set([])
    gs = f.readline()
    while gs:
        set1.add(gs)
        gs = f.readline()

with open(filename, 'r', encoding='utf8') as f:
    set1 = set([])
    gs = f.readline()
    while gs:
        set1.add(gs)
        gs = f.readline()

with open(filename2, 'w', encoding='utf8') as f:
    for gs in set1:
        # print(gs)
        f.write(gs)
        f.write('\n')
