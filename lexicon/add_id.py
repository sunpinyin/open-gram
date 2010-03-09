#!/usr/bin/env python

from __future__ import with_statement
import codecs
from optparse import OptionParser

def normalize_py(py):
    '''convert cc-cedicts py notation to that of sunpinyin
    '''
    if py.find(':') != -1:
        return py.replace('u:e', 'ue').replace('u:', 'v')
    else:
        return py

def init_hanzi_table():
    hanzi_table = {}
    with codecs.open('hanzi_table.utf8', 'r', 'utf-8') as f:
        for line in f:
            hz, pys = line.split(' ', 1)
            hanzi_table[hz] = pys
            
    return hanzi_table

hanzi_table = init_hanzi_table()

def get_hanzi_py(hz, last_py, n_saw):
    try:
        py = hanzi_table[hz] if n_saw > 1 else last_py
    except:
        print '===>', hz
    return normalize_py(py.strip())

def main(fname_in, fname_out):
    dict_in = codecs.open(fname_in, 'r', 'utf-8')
    dict_out = codecs.open(fname_out, 'w', 'utf-8')
    index = 100
    with codecs.open('dict_head.utf8', 'r', 'utf-8') as dict_head:
        head = dict_head.read()
        dict_out.write(head)
    
    last_hz = ''
    last_py = None
    n_saw = 0
    for line in dict_in:
        word, pys = line.split()
        if last_hz:
            if word != last_hz:
                py = get_hanzi_py(last_hz, last_py, n_saw)
                print >> dict_out, last_hz, index, py
                n_saw = 0
                last_hz = ''
                index += 1
            else:
                n_saw += 1
                continue
        
        if len(word) == 1:
            last_hz = word
            last_py = pys
            n_saw = 1
            continue
        pys = "'".join([normalize_py(py) for py in pys.split("'")])
        print >> dict_out, word, index, pys
        index += 1
    if last_hz:
        py = get_hanzi_py(last_hz, last_py, n_saw)
        print >> dict_out, last_hz, index, py

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fr"),
    parser.add_option("-t", "--to")
    opts, args = parser.parse_args()
    main(opts.fr, opts.to)
