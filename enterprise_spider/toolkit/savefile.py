import os


def savefile(filename, text, model='w'):
    seps = filename.split('/')
    if len(seps) == 1:
        seps = filename.split('\\')
    dir_ = '/'.join(seps[:-1])
    os.makedirs(dir_, exist_ok=True)
    with open(filename, model, encoding='utf8') as f:
        f.write(text)
