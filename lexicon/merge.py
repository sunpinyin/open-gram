#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import codecs
import operator
from optparse import OptionParser
from search_filter import get_search_engine
from pinyin import word2pinyin

get_word_freq = get_search_engine('baidu')

def merge(in_fname, new_fname, out_fname):
    in_file = codecs.open(in_fname, 'r', 'utf-8')
    existing_words = set()
    for line in in_file:
        word, py, freq = line.split()
        existing_words.add(word)
        
    new_file = codecs.open(new_fname, 'r', 'utf-8')
    new_words = set()
    for line in new_file:
        word = line.strip()
        new_words.add(word)

    new_words -= existing_words

    out_file = codecs.open(out_fname, 'w', 'utf-8')
    get_word_freq = get_search_engine('baidu')
    for w in new_words:
        py = word2pinyin(w)
        freq = get_word_freq(w)
        print w, py, freq
        print >> out_file, w, py, freq
        
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fr"),
    parser.add_option("-n", "--new"),
    parser.add_option("-t", "--to")
    opts, args = parser.parse_args()
    merge(opts.fr, opts.new, opts.to)

