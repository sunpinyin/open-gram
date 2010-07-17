#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import with_statement
import codecs
from optparse import OptionParser

def normalize_py(py):
    '''convert cc-cedicts py notation to that of sunpinyin
    '''
    py = py.replace(u'üe', u'ue')
    if py.find(':') != -1:
        py = py.replace('u:e', 'ue')
        if py.endswith('u:'):
            py = py.replace('u:', 'v')
    parts = py.split(':')
    py = parts[0]
    if py[-1] in '012345':
        parts[0] = py[:-1]
    return ':'.join(parts)

def normalize_pys(pys):
    return "'".join([normalize_py(py) for py in pys.split("'")])

def main(fname_in, fname_out):
    dict_in = codecs.open(fname_in, 'r', 'utf-8')
    dict_out = codecs.open(fname_out, 'w', 'utf-8')
    index = 100
    with codecs.open('dict_head.utf8', 'r', 'utf-8') as dict_head:
        head = dict_head.read()
        dict_out.write(head)
    
    for line in dict_in:
        word, syls = line.split(' ', 1)
        syls = ' '.join(normalize_pys(pys) for pys in syls.split())
        print >> dict_out, word, index, syls
        index += 1

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fr"),
    parser.add_option("-t", "--to")
    opts, args = parser.parse_args()
    main(opts.fr, opts.to)
