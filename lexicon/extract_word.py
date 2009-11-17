#!/usr/bin/python
# -*- encoding: utf-8 -*-

#
# extract word from segmented corpus, and filter it using a given dictionary
#
# the output will be list of (word, freq)

from __future__ import with_statement
import codecs
import os, sys
from optparse import OptionParser

import wordb
import baseseg
from hanzi_util import is_zh, is_punct
from stopword_filter import is_not_stop_word
from search_filter import get_search_engine

db = wordb.open('./words.db')

verbose = False

#
# filters: returns True if we want keep this word
#
def is_not_single_character(word):
    return len(word) > 1

def is_chinese_word(word):
    return word and is_zh(word[0])

def is_not_known_word(word):
    global db
    return word not in db

filters = [is_not_single_character,
           is_chinese_word,
           is_not_stop_word,
           is_not_known_word]

get_word_freq = None

filter_names = {id(is_not_single_character):"is_not_single_character",
                id(is_chinese_word):"is_chinese_word",
                id(is_not_stop_word):"is_not_stop_word",
                id(is_not_known_word):"is_not_known_word"}

def log(message):
    global verbose
    if verbose:
        print message

def process_words(words, threshold=2560000):
    global get_word_freq
    global db

    for word in words:
        for i, keep_the_word in enumerate(filters):
            if not keep_the_word(word):
                log("%s\tgets killed by %s" % (word, filter_names[id(keep_the_word)]))
                break
        else:
            log("%s\tadded into db" % word)
            if get_word_freq is not None:
                freq = get_word_freq(word)
                if freq > threshold:
                    db[word] = freq
            else:
                db[word] = 1
    
def process_file(input_file):
    words = set()
    for line in input_file:
        words.add(set(line.split(u'/')))
    process_words(words)

def process_files(files, search_engine):
    for fn in files:
        with codecs.open(fn, 'r', 'utf-8') as f:
            process_file(f)

def extract_using_crf():
    default_datadir = '../data'
    default_model = os.path.join(default_datadir , 'model', 'pku-6-tags.model')

    parser = OptionParser()
    parser.add_option("-s", "--search-engine",
                      dest="search_engine")
    parser.add_option("-i", "--input")
    parser.add_option("-m", "--model", default=default_model)
    parser.add_option("-v", "--verbose", action="store_true", default=False)
    opts, args = parser.parse_args()
        
    if opts.input:
        input_files = [opts.input]
    else:
        input_files = args
        
    if opts.search_engine is not None:
        get_word_freq = get_search_engine(search_engine)

    global verbose
    verbose = opts.verbose      
    baseseg.process(opts.model, verbose=False,
                    input_files=input_files,
                    dump_func=process_words)

if __name__ == "__main__":
    extract_using_crf()
    
