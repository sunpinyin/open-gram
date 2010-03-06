#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import codecs
import operator
from optparse import OptionParser


def shrink(in_fname, out_fname):
    in_file = codecs.open(in_fname, 'r', 'utf-8')
    out_file = codecs.open(out_fname, 'w', 'utf-8')
    words_in = 0
    words_out = 0
    for line in in_file:
        word, py, freq = line.split()
        words_in += 1
        if len(word) > 1 and int(freq) < 8000:
            pass
        else:
            words_out += 1
            print >> out_file, word, py
    print "%d => %d" % (words_in, words_out)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fr"),
    parser.add_option("-t", "--to")
    opts, args = parser.parse_args()
    shrink(opts.fr, opts.to)
