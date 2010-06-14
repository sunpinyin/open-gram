#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import codecs
import operator
from optparse import OptionParser

def init_stroke_dict():
    stroke_dict = {}
    with codecs.open('bh.txt', 'r', 'utf-8') as f:
        i = 1
        for line in f:
            hz, strokes = line.split()
            i += 1
            stroke_dict[hz] = int(strokes)
    return stroke_dict

strokes = init_stroke_dict()

def word_cmp(w1, w2):
    zipped = zip(w1, w2)
    for hz1, hz2 in zipped:
        s1 = strokes[hz1]
        s2 = strokes[hz2]
        if s1 < s2:
            return -1
        elif s1 > s2:
            return 1

        s1 = ord(hz1)
        s2 = ord(hz2)
        if s1 < s2:
            return -1
        elif s1 > s2:
            return 1
            
    l1 = len(w1)
    l2 = len(w2)
    if l1 < l2:
        return -1
    elif l1 > l2:
        return 1
    else:
        return 0

def main(input_f, output_f):
    words = []
    with codecs.open(input_f, 'r', 'utf-8') as f:
        for line in f:
            try:
                parts = line.split()
                word = parts[0]
                freq = parts[-1]
                py = parts[1:-1]
                words.append((word, py, freq))
            except Exception, e:
                print e, line

    print len(words), "sorted"
    words.sort(key=operator.itemgetter(0), cmp=word_cmp)
    
    with codecs.open(output_f, 'w', 'utf-8') as f:
        for word, py, freq in words:
            print >> f, word, py, freq
    
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fr"),
    parser.add_option("-t", "--to")
    opts, args = parser.parse_args()
    main(opts.fr, opts.to)
